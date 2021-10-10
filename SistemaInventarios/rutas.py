from flask import Flask, render_template, redirect, request, flash
from SistemaInventarios.dashboard import appDash
import os

#app= Flask(__name__)
appDash.secret_key= os.urandom(32)

datosUsuarios = {
    "Yolima": "1234",
    "Camila": "1234",
    "Jose": "1234",
    "Ricardo": "1234",
    "Jorge": "1234"
}


@appDash.server.route('/', methods=['GET'])
def index():
    return redirect("/index")


@appDash.server.route('/index', methods=('GET', 'POST'))
def login():
    return render_template("index.html")


@appDash.server.route('/validarLogin', methods=('GET', 'POST'))
def validarLogin():
    global usuarios
    if request.method == 'POST':
        # Entra cuando el llamado es hecho por metodo POST.
        userName = request.form['username']
        password = request.form['password']
        if userName in datosUsuarios and password == datosUsuarios[userName]:
            return render_template("Inicio.html")
        else:
            flash("Datos de ingreso incorrectos")
            # mensaje = "Datos de ingreso incorrectos"
            # return render_template("index.html", mensajeInformativo=mensaje)
            return redirect("/index")
    else:
        # Entra cuando el llamado es hecho por metodo GET.
        return redirect("/index")


@appDash.server.route('/inicio', methods=['GET'])
def inicio():
    return render_template("Inicio.html")


@appDash.server.route('/usuarios', methods=('GET','POST'))
def usuarios():
    return render_template("Usuarios.html")


@appDash.server.route('/proveedores', methods=('GET','POST'))
def proveedores():
    return render_template("Proveedores.html")


@appDash.server.route('/productos', methods=('GET','POST'))
def productos():
    return render_template("Productos.html")

"""
@appDash.server.route('/dashboard', methods=['GET'])
def dashBoard():
    return render_template("DashBoard.html")
"""

@appDash.server.route('/dashboard')
def dashboard():
    return appDash.index()


@appDash.server.route('/buscarUsuarios', methods=('GET','POST'))
def buscarUsuarios():
    global usuarios
    if request.method == 'POST':
        tipoBusqueda = request.form['tipoBusqueda']
        textoBuscar = request.form['textoBuscar']
        print("tipoBusqueda: ", tipoBusqueda)
        print("textoBuscar: ", textoBuscar)
        # return render_template("Inicio.html")
        return redirect("/index")
    else:
        return redirect("/index")


# if __name__=='__main__':
#    appDash.run(debug=True)

