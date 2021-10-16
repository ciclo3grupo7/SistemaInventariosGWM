from flask import Flask, render_template, redirect, request, flash, jsonify, make_response
from SistemaInventarios.dashboard import appDash
from SistemaInventarios import db
import os

def miFlash(mensaje):
    flash(mensaje+". ")

def opcBusquedaHTML(listBusqueda, campoSelec=""):
    opciones = ""
    for campo,opc in listBusqueda.items():
        if campo == campoSelec:
            txtSelected = "selected"
        else:
            txtSelected = ""
        opciones += f'<option value="{campo}" {txtSelected}>{opc[0]}</option>'
    # print("opciones: ", opciones)
    return(opciones)

#app= Flask(__name__)
appDash.secret_key= os.urandom(32)
appDash.server.secret_key= os.urandom(32)

datosUsuarios = {
    "Yolima": "1234",
    "Camila": "1234",
    "Jose": "1234",
    "Ricardo": "1234",
    "Jorge": "1234"
}
# Interacción de Proveedores
cabeceraProv = ("Nit","Razón Social","Dirección","Telefono","email","estado","acciones")

datosProveedores = [("1","Proveedor1","Call 43","2233","s@g.com","Activo"),
    ("2","Proveedor2","Call 44","564","t@s.com","Activo")]

datosProveedores.append(("3","Proveedor3","Call 44","564","t@s.com","Activo"))

# Interacción de Usuarios
cabeceraUsuar = ("Usuario","Nombre","Perfil","Estado","acciones")

datosUsuar = [("jserge","José Serge","Administrador","Activo"),
    ("yperez","Yolima Perez","SuperAdministrador","Activo"),
    ("jmunoz","Jorge Muñoz","Usuario Final","Activo")]

datosUsuar.append(("rmillan","Ricardo Millan","SuperAdministrador","Activo"))

# Interacción de Productos
cabeceraProd = ("Identificador","Nombre"," Cantidad Minima","Cantidad Disponible","Descripcion","Estado","acciones")

datosProductos = [(1,"Carro Toyota Prado",2,0,"Modelo 2018, automatico","Activo"),
    (2,"Carro Hyundai Tucson",4,1,"Modelo 2021, mecanico","Activo"),(3,"Carro Mazda 5",2,1,"Modelo 2017 automatico","Activo")]


listaBusquedaUsuarios = {
    "usuario": ["Usuario","=="],
    "nombre": ["Nombre","in"],
    "tipoUsuario": ["Perfil","=="],
    "estado": ["Estado","=="],
}
opcionesUsuarios = opcBusquedaHTML(listaBusquedaUsuarios)

listaBusquedaProveedores = {
    "nit": ["Nit", "=="],
    "nombre": ["Razon Social", "in"],
    "direccion": ["Direccion", "in"],
    "telefono": ["Telefono", "in"],
    "email": ["Email", "in"],
    "estado": ["Estado", "=="],
}
opcionesProveedores = opcBusquedaHTML(listaBusquedaProveedores)

listaBusquedaProductos = {
    "idProducto": ["Identificador", "=="],
    "nombre": ["Nombre", "In"],
    "descripcion": ["Descripcion", "in"],
    "estado": ["Estado", "=="],
}
opcionesProductos = opcBusquedaHTML(listaBusquedaProductos)

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
        datUsuario = next((x for x in db.datosUsuarios if x["usuario"] == userName), None)

        if datUsuario != None and datUsuario["clave"] == password:
            return render_template("Inicio.html")
        else:
            miFlash("Datos de ingreso incorrectos")
            # mensaje = "Datos de ingreso incorrectos"
            # return render_template("index.html", mensajeInformativo=mensaje)
            return redirect("/index")
    else:
        # Entra cuando el llamado es hecho por metodo GET.
        return redirect("/index")


@appDash.server.route('/inicio', methods=['GET'])
def inicio():
    return render_template("Inicio.html")

#USUARIOS JMSS
@appDash.server.route('/usuarios', methods=('GET','POST'))
def usuarios():
    global opcionesUsuarios, cabeceraUsuar
    return render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opcionesUsuarios)


@appDash.server.route('/ValidarBusquedaUser', methods=('GET','POST'))
def ValidarBusquedaUser():
    #JHMO
    global listaBusquedaUsuarios, opcionesUsuarios, cabeceraUsuar
    if request.method == 'POST':
        campoBuscar = request.form['select']
        texto = request.form['text'].upper().strip()
        tipoBusqueda = listaBusquedaUsuarios[campoBuscar][1]

        if len(texto) > 0:
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosUsuarios))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosUsuarios))
        else:
            listRta = list(db.datosUsuarios)
        #print(listRta)

        if len(listRta) > 0:
            miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = make_response(render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, data=listRta))
        else:
            miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = make_response(render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones))

        rtaHTML.set_cookie('campoBuscarUsr', campoBuscar)
        rtaHTML.set_cookie('textoBuscarUsr', texto)
        return rtaHTML
    else:
        return redirect("/usuarios")


@appDash.server.route('/ajaxUsuarioMod', methods=('GET','POST'))
def ajaxUsuarioMod():
    global opcionesUsuarios, cabeceraUsuar
    if request.method == 'POST':
        idUsuario = request.form['id']
        #print("idUsuario:",idUsuario)
        usuario = db.buscarUsuario(idUsuario)
        #
        if usuario.tipoUsuario == "UsuarioFinal":
            usuario.tipoUsuario1 = "selected"
        elif usuario.tipoUsuario == "Administrador":
            usuario.tipoUsuario2 = "selected"
        elif usuario.tipoUsuario == "SuperAdministrador":
            usuario.tipoUsuario3 = "selected"
        #            
        if usuario.estado == "Activo":
            usuario.estado1 = "selected"
        else:
            usuario.estado2 = "selected"
        #            
        if usuario.cambiarClave == "1":
            usuario.cambiarClaveChk = "checked"
        else:
            usuario.cambiarClaveChk = ""

        #print("usuario.idUsuario:",usuario.idUsuario)
        #return jsonify({'htmlresponse': render_template('modUsuarios.html',infoUsuario=usuario)})
        rtaHTML = render_template('modUsuarios.html',infoUsuario=usuario)
        #f = open("./xx_modUsuarios.html","w")
        #f.write(xhtml)
        #f.close()
        return jsonify({'htmlresponse': rtaHTML})
    else:
        return redirect("/usuarios")
 

@appDash.server.route('/ajaxUsuarioEli', methods=('GET','POST'))
def ajaxUsuarioEli():
    global opcionesUsuarios, cabeceraUsuar
    print("entro /ajaxUsuarioEli")
    if request.method == 'POST':
        print("entro /ajaxUsuarioEli POST")
        idUsuario = request.form['id']
        print("idUsuario:",idUsuario)
        usuario = db.buscarUsuario(idUsuario)

        rtaHTML = render_template('eliUsuarios.html',infoUsuario=usuario)
        return jsonify({'htmlresponse': rtaHTML})
    else:
        return redirect("/usuarios")


@appDash.server.route('/modificarUsuarios', methods=('GET','POST'))
def modificarUsuarios():
    global opcionesUsuarios, cabeceraUsuar
    #print("entro /modificarUsuarios")
    if request.method == 'POST':
        #print("entro /modificarUsuarios POST")
        # OJO. Los campos tipo "checkbox" solo son retornando en el form cuando fueron marcados, 
        # de lo contrario no se crean en la lista de campos del form.
        datosUsuario = {
            'idUsuario': request.form['idUsuario'],
            'cedula': request.form['cedula'],
            'usuario': request.form['usuario'],
            'nombre': request.form['nombre'],
            #'apellido': request.form['apellido'],
            'email': request.form['email'],
            'direccion': request.form['direccion'],
            'tipoUsuario': request.form['tipoUsuario'],
            'estado': request.form['estado'],
            'clave': request.form['clave'],
            'cambiarClave': ("1" if 'cambiarClave' in request.form else "0"),
        }
        usuario = db.Usuario(datosUsuario)
        rta = db.actualizarUsuario(usuario)
        #print("db.datosUsuarios",db.datosUsuarios)
        if rta == 1:
            miFlash("Se inserto un registro")
        else:
            miFlash("Registro Actualizado")

        # cargar datos de busqueda desde las cookies.
        campoBuscar = request.cookies.get('campoBuscarUsr')
        texto = request.cookies.get('textoBuscarUsr')
        tipoBusqueda = listaBusquedaUsuarios[campoBuscar][1]

        if len(texto) > 0:
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosUsuarios))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosUsuarios))
        else:
            listRta = list(db.datosUsuarios)

        if len(listRta) > 0:
            #miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, data=listRta)
        else:
            #miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones)

        return rtaHTML

    else:
        return redirect("/usuarios")


@appDash.server.route('/eliminarUsuario', methods=('GET','POST'))
def eliminarUsuario():
    global opcionesUsuarios, cabeceraUsuar
    #print("entro /eliminarUsuario")
    if request.method == 'POST':
        #print("entro /eliminarUsuario POST")
        # OJO. Los campos tipo "checkbox" solo son retornando en el form cuando fueron marcados, 
        # de lo contrario no se crean en la lista de campos del form.
        idUsuario= request.form['idUsuario']
        sino= request.form['sino']
        #print("idUsuario", idUsuario)
        #print("sino", sino)

        if sino == "Si":
            rta = db.eliminarUsuario(idUsuario)
            #print("rta db.eliminarUsuario(idUsuario)",rta)
            if rta == 1:
                miFlash("Registro Eliminado")
            else:
                miFlash("Registro NO encontrado")

        # cargar datos de busqueda desde las cookies.
        campoBuscar = request.cookies.get('campoBuscarUsr')
        texto = request.cookies.get('textoBuscarUsr')
        tipoBusqueda = listaBusquedaUsuarios[campoBuscar][1]

        if len(texto) > 0:
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosUsuarios))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosUsuarios))
        else:
            listRta = list(db.datosUsuarios)

        if len(listRta) > 0:
            #miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, data=listRta)
        else:
            #miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones)

        return rtaHTML

    else:
        return redirect("/usuarios")


#PRODUCTOS PROVEEDORES
@appDash.server.route('/proveedores', methods=('GET','POST'))
def proveedores():
    global opcionesProveedores, cabeceraProv
    return render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opcionesProveedores)

@appDash.server.route('/buscarProveedores', methods=('GET','POST'))
def buscarproveedores():
    #JHMO
    global listaBusquedaProveedores, opcionesProveedores, cabeceraProv
    if request.method == 'POST':
        campoBuscar = request.form['select']
        texto = request.form['text'].upper().strip()
        tipoBusqueda = listaBusquedaProveedores[campoBuscar][1]

        if len(texto) > 0:
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosProveedores))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosProveedores))
        else:
            listRta = list(db.datosProveedores)

        if len(listRta) > 0:
            data = []
            for x in listRta:
                valores = list(x.values())
                # Se quita la columna de Id
                del valores[0]
                # Se adiciona al resultado
                data.append(valores)
            miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            return render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, data=data)
        else:
            miFlash("Datos No Encontrados")
            return render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opcionesProveedores)
    else:
        return render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opcionesProveedores)
                   

@appDash.server.route('/insertarProveedor', methods=('GET','POST'))
def insertarproveedor():
    if request.method == 'POST':
        # Entra cuando el llamado es hecho por metodo POST.
        
        nit = request.form['nit']
        razonSocial = request.form['razon-social']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        estado = request.form['estado']
        #print("Los datos a ingresar son :",nit, razonSocial,direccion, telefono,email,estado)
        
        #RJMM se tiene en cuenta en caso de agregar, nuevos proveedores
        tam = (len(datosProveedores))
        existe = "NO"
        indice = 0
        for i in range(tam):
            if datosProveedores[i][0]==nit:
                existe = "SI"
                indice = i              

        if existe == "SI":
                miFlash("Registro Actualizado")
                datosProveedores.pop(indice)
                datosProveedores.append((nit,razonSocial,direccion, telefono,email,estado))
        else:
            datosProveedores.append((nit,razonSocial,direccion, telefono,email,estado))
            miFlash("Se inserto un registro")
            
        return redirect("/proveedores")        

#PRODUCTOS LOGICA

@appDash.server.route('/productos', methods=('GET','POST'))
def productos():
    global opcionesProductos, cabeceraProd
    # return render_template("Productos.html")
    return render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opcionesProductos)

@appDash.server.route('/buscarProductos', methods=('GET','POST'))
def buscarproductos():
    #JHMO
    global listaBusquedaProductos, opcionesProductos, cabeceraProd
    if request.method == 'POST':
        campoBuscar = request.form['select']
        texto = request.form['text'].upper().strip()
        tipoBusqueda = listaBusquedaProductos[campoBuscar][1]

        if len(texto) > 0:
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar] == texto, db.datosProductos))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosProductos))
        else:
            listRta = list(db.datosProductos)

        if len(listRta) > 0:
            data = []
            for x in listRta:
                valores = list(x.values())
                data.append(valores)
            miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            return render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, data=data)
        else:
            miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            return redirect("Productos.html", headings=cabeceraProd, opcBusqueda=opciones)
    else:
        return redirect("Productos.html", headings=cabeceraProd, opcBusqueda=opcionesProductos)


#metodo insertar producto
@appDash.server.route('/insertarProducto', methods=('GET','POST'))
def insertarproducto():
    if request.method == 'POST':
        # Entra cuando el llamado es hecho por metodo POST.
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        cantidadMinima = request.form['c-minima']
        cantidadDisponible = request.form['c-disponible']
        descripcion = request.form['comment']
        estado = request.form['select']
        
               
        tam = (len(datosProductos))
        existe = "NO"
        indice = 0
        for i in range(tam):
            if datosProductos[i][0]==int(codigo):
                existe = "SI"
                indice = i              

        if existe == "SI":
                miFlash("Registro Actualizado")
                datosProductos.pop(indice)
                datosProductos.append((int(codigo),nombre,int(cantidadMinima),int(cantidadDisponible),descripcion,estado))
        else:
            datosProductos.append((int(codigo),nombre,int(cantidadMinima),int(cantidadDisponible),descripcion,estado))
            miFlash("Se inserto un registro")
            
        return redirect("/productos") 


@appDash.server.route('/dashboard')
def dashboard():
    return appDash.index()

# if __name__=='__main__':
#    appDash.run(debug=True)

