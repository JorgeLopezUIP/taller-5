from flask import Flask, render_template, request,redirect,url_for
import redis, os

keydb = redis.Redis(host="localhost", port=6380, decode_responses=True)

app = Flask(__name__, template_folder= "templates")
app.secret_key = os.urandom(16)


@app.route("/", methods = ["GET", "POST"])
def index(): 
     libros = {}
     for key in keydb.keys("libro:*"): 
        if not key.endswith("id"):
            libro = keydb.hgetall(key)
            libros[key] = libro
     return render_template("index.html", libros = libros)

@app.route("/registro",methods = ["POST", "GET"]) 
def registrar_libro(): 
    if request.method == "POST": 
        nombre = request.form["nombre"]
        genero = request.form["genero"]
        autor = request.form["autor"]
        
        libro_id = keydb.incr("libro:id")
        key = f"libro:{libro_id}"

        keydb.hset(key, mapping= {"libro": nombre, "genero": genero, "autor": autor}) 
        return render_template("registro.html")
        
        
    return render_template("registro.html")


@app.route("/eliminar/<int:index>") 
def eliminar_libro(index): 
    keydb.delete(f"libro:{index}")
    return redirect(url_for("index"))

@app.route("/editar/<int:index>",methods = ["POST", "GET"]) 
def editar_libro(index): 
    key = f"libro:{index}"
    if request.method == "POST": 
        nuevo_nombre = request.form["nombre"]
        nuevo_genero = request.form["genero"]
        nuevo_autor = request.form["autor"]

        keydb.hset(key, mapping={
                   "libro": nuevo_nombre,
                   "genero": nuevo_genero, 
                   "autor": nuevo_autor
                   })
        return redirect(url_for("index")) 
    
    datos_libro = keydb.hgetall(key)
    return render_template("editar.html", libro = datos_libro, libro_id = index)    
        
    
if __name__ == "__main__":
    app.run(debug=True)


    