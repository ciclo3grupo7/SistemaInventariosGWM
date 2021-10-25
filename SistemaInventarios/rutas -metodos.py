from flask import Flask, render_template, redirect, request, flash, jsonify, make_response, session
from SistemaInventarios.dashboard import appDash
from SistemaInventarios.dashboard import dashboard_principal
from SistemaInventarios import db
import os
#from SistemaInventarios import serverFlask

from SistemaInventarios.modelsDB import *
from SistemaInventarios.config import dev2
import SistemaInventarios.crud as crud
#from SistemaInventarios import serverFlask

appDash.server.config.from_object(dev2)


bd.init_app(appDash.server)

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

def opcMenuHTML(permisosUsuario):
    opcMenu = ""
    if "ver" in permisosUsuario["Usuarios"]:
        opcMenu += '<li class="u-nav-item"><a class="u-button-style u-nav-link" href="/usuarios">Usuarios</a></li>\n'
    if "ver" in permisosUsuario["Proveedores"]:
        opcMenu += '<li class="u-nav-item"><a class="u-button-style u-nav-link" href="/proveedores">Proveedores</a></li>\n'
    if "ver" in permisosUsuario["Productos"]:
        opcMenu += '<li class="u-nav-item"><a class="u-button-style u-nav-link" href="/productos">Productos</a></li>\n'
    if "ver" in permisosUsuario["Dashboard"]:
        opcMenu += '<li class="u-nav-item"><a class="u-button-style u-nav-link" href="/dashboard">Dashboard</a></li>\n'
    opcMenu += '<li class="u-nav-item"><a class="u-button-style u-nav-link" href="/cerrarSesion">Cerrar Sesión</a></li>\n'
    #print("opcionesMenu: ", opcMenu)
    return(opcMenu)


#app= Flask(__name__)
appDash.secret_key= os.urandom(32)
appDash.server.secret_key= os.urandom(32)

#Configuracion del servidor Flask
#appDash.server.config.from_object(dev)

#toma la conf que acaba de pasar
#bd.init_app(appDash.server)


# Interacción de Proveedores
cabeceraProv = ("Nit","Razón Social","Dirección","Telefono","email","estado","acciones")

# Interacción de Usuarios
cabeceraUsuar = ("Usuario","Nombre","Perfil","Estado","acciones")


# Interacción de Productos
cabeceraProd = ("Identificador","Nombre"," Cantidad Minima","Cantidad Disponible","Descripcion","Estado","acciones")

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
    rtaHTML = make_response(render_template("index.html"))
    return rtaHTML


@appDash.server.route('/cerrarSesion', methods=('GET', 'POST'))
def cerrarSesion():
    # Borra las variables de sesión creadas
    session.clear()
    #rtaHTML = make_response(render_template("index.html"))
    #return rtaHTML
    return redirect("/index")


@appDash.server.route('/validarLogin', methods=('GET', 'POST'))
def validarLogin():
    global usuarios
    if request.method == 'POST':
        # Entra cuando el llamado es hecho por metodo POST.
        userName = request.form['username']
        password = request.form['password']
        
        # datUsuario = next((x for x in db.datosUsuarios if x['usuario'] == userName), None) 
        usuario = crud.consultar_usuario(usuario = userName)
        #print("usuario:", usuario.usuario, usuario.clave)

        """
        if datUsuario != None and datUsuario['clave'] == password:
            session['usuario'] = datUsuario['usuario']
            session['clave'] = datUsuario['clave']
            session['tipoUsuario'] = datUsuario['tipoUsuario']
        """        
        if usuario != None and usuario.clave == password:
            session['idUsuario'] = usuario.idUsuario
            session['usuario'] = usuario.usuario
            session['clave'] = usuario.clave
            session['tipoUsuario'] = usuario.tipoUsuario
            return redirect("/inicio")
           
        else:
            miFlash("Datos de ingreso incorrectos")
            # Borra las variables de sesión creadas
            session.clear()
            return redirect("/index")

    else:
        # Entra cuando el llamado es hecho por metodo GET.
        return redirect("/index")


@appDash.server.route('/inicio', methods=['GET'])
def inicio():
    if "usuario" in session:
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        rtaHTML = make_response(render_template("Inicio.html", title="Inicio", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu))
        return rtaHTML
    else:
        return redirect("/index")


#LOGICA USUARIOS
@appDash.server.route('/usuarios', methods=('GET','POST'))
def usuarios():
    global opcionesUsuarios, cabeceraUsuar
    
    if "usuario" in session and "ver" in db.permisosUsuario["Usuarios"]:
        # Si inicio sesion y tiene permiso, lo lleva a la opcion correspondiente.
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        return render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opcionesUsuarios, title="Usuarios", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)

    elif "usuario" in session:
        # Si inicio sesion, pero no tiene permiso, lo lleva a la opcion correspondiente.
        return redirect("/inicio")

    else:
        # No inicio sesion
        return redirect("/index")



@appDash.server.route('/buscarUsuarios', methods=('GET','POST'))
def buscarUsuarios():
    #JHMO
    global listaBusquedaUsuarios, opcionesUsuarios, cabeceraUsuar
    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)

        campoBuscar = request.form['select']
        #texto = request.form['text'].upper().strip()
        texto = request.form['text'].strip()
        tipoBusqueda = listaBusquedaUsuarios[campoBuscar][1]

        if len(texto) > 0:
            """
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosUsuarios))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosUsuarios))
            """
            listRta = crud.consultar_usuarios(campoBuscar, texto)
        else:
            #listRta = list(db.datosUsuarios)
            listRta = crud.consultar_usuarios()
        # listRta es un arreglo de diccionarios extraidos de db.datosUsuarios
        #print("listRta:",listRta)

        if len(listRta) > 0:
            miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = make_response(render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, data=listRta, title="Usuarios", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu))
        else:
            miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = make_response(render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, title="Usuarios", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu))

        session['campoBuscarUsr'] = campoBuscar
        session['textoBuscarUsr'] = texto
        return rtaHTML

    else:
        return redirect("/usuarios")


@appDash.server.route('/ajaxUsuarioMod', methods=('GET','POST'))
def ajaxUsuarioMod():
    global opcionesUsuarios, cabeceraUsuar
    if "usuario" in session and request.method == 'POST':
        idUsuario = int(request.form['id'])
        
        if idUsuario == 0:
            # Crear usuario
            #db.maxIdUsuario+=1
            datosUsuario = {
                #"idUsuario": str(db.maxIdUsuario),
                'idUsuario': 0,
                'cedula': "",
                'usuario': "",
                'nombre': "",
                'email': "",
                'direccion': "",
                'tipoUsuario': "UsuarioFinal",
                'estado': "Activo",
                'clave': "",
                'cambiarClave': "1",
                'aceptarPolitica': "1",
            }
            usuario = crud.Usuario(datosUsuario)

        else:
            #usuario = db.buscarUsuario(idUsuario)
            usuario = crud.consultar_usuario(idUsuario=idUsuario)
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
        rtaHTML = render_template('modUsuarios.html',infoUsuario=usuario)
        return jsonify({'htmlresponse': rtaHTML})
    else:
        return redirect("/usuarios")
 

@appDash.server.route('/ajaxUsuarioEli', methods=('GET','POST'))
def ajaxUsuarioEli():
    global opcionesUsuarios, cabeceraUsuar
    #print("entro /ajaxUsuarioEli")
    if "usuario" in session and request.method == 'POST':
        #print("entro /ajaxUsuarioEli POST")
        idUsuario = int(request.form['id'])
        #print("idUsuario:",idUsuario)
        #usuario = db.buscarUsuario(idUsuario)
        usuario = crud.consultar_usuario(idUsuario=idUsuario)
        rtaHTML = render_template('eliUsuarios.html',infoUsuario=usuario)
        return jsonify({'htmlresponse': rtaHTML})
    else:
        return redirect("/usuarios")




@appDash.server.route('/modificarUsuarios', methods=('GET','POST'))
def modificarUsuarios():
    global opcionesUsuarios, cabeceraUsuar
    #print("entro /modificarUsuarios")
    if "usuario" in session and request.method == 'POST':
        idUsuarioLogin = session['idUsuario']
        usuarioLogin = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        #print("entro /modificarUsuarios POST")
        # OJO. Los campos tipo "checkbox" solo son retornando en el form cuando fueron marcados, 
        # de lo contrario no se crean en la lista de campos del form.
        datosUsuario = {
            'idUsuario': int(request.form['idUsuario']),
            'cedula': request.form['cedula'],
            'usuario': request.form['usuario'],
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'direccion': request.form['direccion'],
            'tipoUsuario': request.form['tipoUsuario'],
            'estado': request.form['estado'],
            'clave': request.form['clave'],
            'cambiarClave': ("1" if 'cambiarClave' in request.form else "0"),
            'idUsuarioCrea_id': idUsuarioLogin,
            'idUsuarioEdita_id': idUsuarioLogin,
        }
        usuario = crud.Usuario(datosUsuario)
        #print("modificar usuario.idUsuario:",usuario.idUsuario)
        # Quitar la llave para que no se actualice.
        datosUsuario.pop("idUsuario")
        #rta = db.actualizarUsuario(usuario)

        if usuario.idUsuario == 0:
            # Registro nuevo
            rta = crud.insertar_usuario(datosUsuario)
            #print("rta :",rta)
            if rta > 0:
                miFlash("Se inserto un registro")
            else:
                miFlash("Fallo la creacion del registro")
            #print("rta.insert:",rta)
        else:
            # Quitar idUsuarioCrea_id para que no se actualice cuando el registro ya exite.
            datosUsuario.pop("idUsuarioCrea_id")
            rta = crud.actualizar_usuario(usuario.idUsuario, datosUsuario)
            if rta == 1:
                miFlash("Registro Actualizado")
            else:
                miFlash("Fallo la actualización del registro")
            #print("rta.update:",rta)

        # cargar datos de busqueda desde las cookies.
        if 'campoBuscarUsr' in session:
            campoBuscar = session['campoBuscarUsr']
            texto = session['textoBuscarUsr']
            tipoBusqueda = listaBusquedaUsuarios[campoBuscar][1]
        else:
            campoBuscar = "usuario"
            texto = datosUsuario['usuario']
            tipoBusqueda = "=="

        if len(texto) > 0:
            """
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosUsuarios))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosUsuarios))
            """
            listRta = crud.consultar_usuarios(campoBuscar, texto)
        else:
            #listRta = list(db.datosUsuarios)
            listRta = crud.consultar_usuarios()

        if len(listRta) > 0:
            #miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, data=listRta, title="Usuarios", usuario=usuarioLogin, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)
        else:
            #miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, title="Usuarios", usuario=usuarioLogin, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect("/usuarios")


@appDash.server.route('/eliminarUsuario', methods=('GET','POST'))
def eliminarUsuario():
    global opcionesUsuarios, cabeceraUsuar
    #print("entro /eliminarUsuario")
    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        #print("entro /eliminarUsuario POST")
        # OJO. Los campos tipo "checkbox" solo son retornando en el form cuando fueron marcados, 
        # de lo contrario no se crean en la lista de campos del form.
        idUsuario= int(request.form['idUsuario'])
        sino= request.form['sino']
        #print("eliminar idUsuario", idUsuario)
        #print("sino", sino)

        if sino == "Si":
            #rta = db.eliminarUsuario(idUsuario)
            rta = crud.eliminar_usuario(idUsuario)
            #print("rta db.eliminarUsuario(idUsuario)",rta)
            if rta == 1:
                miFlash("Registro Eliminado")
            else:
                miFlash("Registro NO encontrado")

        # cargar datos de busqueda desde las cookies.
        campoBuscar = session['campoBuscarUsr']
        texto = session['textoBuscarUsr']
        tipoBusqueda = listaBusquedaUsuarios[campoBuscar][1]

        if len(texto) > 0:
            """
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosUsuarios))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosUsuarios))
            """
            listRta = crud.consultar_usuarios(campoBuscar, texto)
        else:
            #listRta = list(db.datosUsuarios)
            listRta = crud.consultar_usuarios()

        if len(listRta) > 0:
            #miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, data=listRta, title="Usuarios", usuario=usuario, opcMenu=opcMenu)
        else:
            #miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaUsuarios, campoBuscar)
            rtaHTML = render_template("Usuarios.html", headings=cabeceraUsuar, opcBusqueda=opciones, title="Usuarios", usuario=usuario, opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect("/usuarios")


#LOGICA PROVEEDORES

@appDash.server.route('/proveedores', methods=('GET','POST'))
def proveedores():
    global opcionesProveedores, cabeceraProv
    if "usuario" in session and "ver" in db.permisosUsuario["Proveedores"]:
        # Si inicio sesion y tiene permiso, lo lleva a la opcion correspondiente.
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']        
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        return render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opcionesProveedores, title="Proveedores", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)

    elif "usuario" in session:
        # Si inicio sesion, pero no tiene permiso, lo lleva a la opcion correspondiente.
        return redirect("/inicio")

    else:
        # No inicio sesion
        return redirect("/index")


@appDash.server.route('/ajaxProveedorMod', methods=('GET','POST'))
def ajaxProveedorMod():
    global opcionesProveedores, cabeceraProv
    if "usuario" in session and request.method == 'POST':
        idProveedor = int(request.form['id'])
        #print("idProveedor:",idProveedor)
        if idProveedor == 0:
            # Crear proveedor
            #db.maxIdProveedor+=1
            datosProveedor = {
                "idProveedor": 0,
                "nit": "",
                "nombre": "",
                "direccion": "",
                "telefono": "",
                "email": "",
                "estado": "Activo",
            }

            #proveedor = db.Proveedor(datosProveedor)
            proveedor = crud.Proveedor(datosProveedor)

        else:
            #proveedor = db.buscarProveedor(idProveedor)
            proveedor = crud.consultar_proveedor(idProveedor)
            
            if proveedor.estado == "Activo":
                proveedor.estado1 = "selected"
            else:
                proveedor.estado2 = "selected"
            
        rtaHTML = render_template('modProveedor.html',infoProveedor=proveedor)

        return jsonify({'htmlresponse': rtaHTML})
    else:
        return redirect("/proveedores")


@appDash.server.route('/ajaxProveedorEli', methods=('GET','POST'))
def ajaxProveedorEli():
    global opcionesProveedores, cabeceraProv

    if "usuario" in session and request.method == 'POST':
        idProveedor = request.form['id']

               
        #proveedor = db.buscarProveedor(idProveedor)
        proveedor = crud.consultar_proveedor(idProveedor)
        rtaHTML = render_template('eliProveedor.html',infoProveedor=proveedor)
        return jsonify({'htmlresponse': rtaHTML})
    else:
        return redirect("/proveedores")


@appDash.server.route('/buscarProveedores', methods=('GET','POST'))
def buscarproveedores():
    global listaBusquedaProveedores, opcionesProveedores, cabeceraProv

    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        campoBuscar = request.form['select']
        texto = request.form['text'].upper().strip()
        tipoBusqueda = listaBusquedaProveedores[campoBuscar][1]

        

        if len(texto) > 0:
            """
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosProveedores))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosProveedores))
            """
            listRta = crud.consultar_proveedores()
        else:
            #listRta = list(db.datosProveedores)
            listRta = crud.consultar_proveedores()
        
        if len(listRta) > 0:
            miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = make_response(render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, data=listRta, title="Proveedores", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario),opcMenu=opcMenu))
        else:
            miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = make_response(render_template("Proveedores.html", headings=cabeceraUsuar, opcBusqueda=opciones, title="Proveedores", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu))

        session['campoBuscarProv'] = campoBuscar
        session['textoBuscarProv'] = texto

        return rtaHTML
    else:
        return redirect("/proveedores")



@appDash.server.route('/modificarProveedor', methods=('GET','POST'))
def modificarProveedor():
    global opcionesProveedores, cabeceraProv
    if "usuario" in session and request.method == 'POST':
        #print("entro modificarProveedor")
        idUsuarioLogin = session['idUsuario']
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        datosProveedor = {
            'idProveedor': int(request.form['idProveedor']),
            'nit': request.form['nit'],
            'nombre': request.form['nombre'],
            'direccion': request.form['direccion'],
            'telefono': request.form['telefono'],
            'email': request.form['email'],
            'estado': request.form['estado'],
            'idUsuarioCrea_id': idUsuarioLogin,
            'idUsuarioEdita_id': idUsuarioLogin,
        }

        
        ## inicia nuevo
        proveedor = crud.Proveedor(datosProveedor)
        datosProveedor.pop("idProveedor")
        #print("proveedor.idProveedor:",proveedor.idProveedor)

        if proveedor.idProveedor == 0:
            # Registro nuevo
            rta = crud.insertar_proveedor(datosProveedor)
            #print("rta :",rta)
            if rta > 0:
                miFlash("Se inserto un registro")
            else:
                miFlash("Fallo la creacion del registro")
            #print("rta.insert:",rta)
        else:
            # Quitar idUsuarioCrea_id para que no se actualice cuando el registro ya exite.
            datosProveedor.pop("idUsuarioCrea_id")
            rta = crud.actualizar_proveedor(proveedor.idProveedor, datosProveedor)
            if rta == 1:
                miFlash("Registro Actualizado")
            else:
                miFlash("Fallo la actualización del registro")
            #print("rta.update:",rta)

        # cargar datos de busqueda desde las cookies.
        if 'campoBuscarProv' in session:
            campoBuscar = session['campoBuscarProv']
            texto = session['textoBuscarProv']
            tipoBusqueda = listaBusquedaProveedores[campoBuscar][1]
        else:
            campoBuscar = "nombre"
            texto = datosProveedor['nombre']
            tipoBusqueda = "=="
        ## fin nuevo ##

        if len(texto) > 0:
            """
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosProveedores))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosProveedores))
            """
            listRta = crud.consultar_proveedores(campoBuscar, texto)
        else:
            #listRta = list(db.datosProveedores)
            listRta = crud.consultar_proveedores()

        if len(listRta) > 0:
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, data=listRta, title="Proveedores", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)
        else:
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, title="Proveedores", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect("/proveedores")




@appDash.server.route('/eliminarProveedor', methods=('GET','POST'))
def eliminarProveedor():
    global opcionesProveedores, cabeceraProv
  
    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        idProveedor= request.form['idProveedor']
        sino= request.form['sino']

        

        if sino == "Si":

            #rta = db.eliminarProveedor(idProveedor)
            rta = crud.eliminar_Proveedor(idProveedor)
            
            if rta == 1:
                miFlash("Registro Eliminado")
            else:
                miFlash("Registro NO encontrado")

        # cargar datos de busqueda desde las cookies.
        campoBuscar = session['campoBuscarProv']
        texto = session['textoBuscarProv']
        tipoBusqueda = listaBusquedaProveedores[campoBuscar][1]

        if len(texto) > 0:
            """"
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosProveedores))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosProveedores))
            """
            listRta = crud.consultar_proveedores(campoBuscar, texto)
        else:
            #listRta = list(db.datosProveedores)
            listRta = crud.consultar_proveedores()

       
            

        if len(listRta) > 0:
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, data=listRta, title="Proveedores", usuario=usuario, opcMenu=opcMenu)
        else:
            opciones = opcBusquedaHTML(listaBusquedaProveedores, campoBuscar)
            rtaHTML = render_template("Proveedores.html", headings=cabeceraProv, opcBusqueda=opciones, title="Proveedores", usuario=usuario, opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect("/proveedores")



#LOGICA PRODUCTOS

@appDash.server.route('/productos', methods=('GET','POST'))
def productos():
    global opcionesProductos, cabeceraProd
    if "usuario" in session and "ver" in db.permisosUsuario["Productos"]:
        # Si inicio sesion y tiene permiso, lo lleva a la opcion correspondiente.
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        return render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opcionesProductos, title="Productos", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)
    
    elif "usuario" in session:
        # Si inicio sesion, pero no tiene permiso, lo lleva a la opcion correspondiente.
        return redirect("/inicio")

    else:
        return redirect("/index")


@appDash.server.route('/ajaxProductoMod', methods=('GET','POST'))
def ajaxProductoMod():
    global opcionesProductos, cabeceraProd
    if "usuario" in session and request.method == 'POST':
        idProducto = request.form['id']
        if idProducto == "0":
            # Crear producto
            db.maxIdProducto+=1
            datosProveedor = {
                "idProducto": str(db.maxIdProveedor),
                "nombre": "",
                "cantMin": "",
                "cantBodega": "",
                "descripcion": "",
                "estado": "Activo",
            }

            producto = db.Producto(datosProveedor)

        else:
            producto = db.buscarProducto(idProducto)
        
        if producto.estado == "Activo":
            producto.estado1 = "selected"
        else:
            producto.estado2 = "selected"
            
        rtaHTML = render_template('modProducto.html',infoProducto=producto)

        return jsonify({'htmlresponse': rtaHTML})
    else:
        return redirect("/productos")


@appDash.server.route('/ajaxProductoEli', methods=('GET','POST'))
def ajaxProductoEli():
    global opcionesProductos, cabeceraProd
   
    if "usuario" in session and request.method == 'POST':
        idProducto = request.form['id']
        producto = db.buscarProducto(idProducto)
        rtaHTML = render_template('eliProducto.html',infoProducto=producto)
        return jsonify({'htmlresponse': rtaHTML})
    else:
        return redirect("/productos")


@appDash.server.route('/buscarProductos', methods=('GET','POST'))
def buscarProductos():
    global listaBusquedaProductos, opcionesProveedores, cabeceraProd

    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        campoBuscar = request.form['select']
        texto = request.form['text'].upper().strip()
        tipoBusqueda = listaBusquedaProductos[campoBuscar][1]

        if len(texto) > 0:
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosProductos))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosProductos))
        else:
            listRta = list(db.datosProductos)
        
        if len(listRta) > 0:
            miFlash("Datos Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = make_response(render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, data=listRta, title="Productos", usuario=usuario, infoUser = (usuario+" - "+tipoUsuario),opcMenu=opcMenu))
        else:
            miFlash("Datos No Encontrados")
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = make_response(render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, title="Productos", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu))

        session['campoBuscarProd'] = campoBuscar
        session['textoBuscarProd'] = texto
        return rtaHTML

    else:
        return redirect("/productos")



@appDash.server.route('/modificarProducto', methods=('GET','POST'))
def modificarProducto():
    global opcionesProductos, cabeceraProd
   
    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        datosProducto = {
            'idProducto': request.form['idProducto'],
            'nombre': request.form['nombre'],
            'cantMin': request.form['cantMin'],
            'cantBodega': request.form['cantBodega'],
            'descripcion': request.form['descripcion'],
            'estado': request.form['estado'],
            
        }
        producto = db.Producto(datosProducto)
        rta = db.actualizarProducto(producto)
        
        if rta == 1:
            miFlash("Se inserto un registro")
        else:
            miFlash("Registro Actualizado")

        campoBuscar = session['campoBuscarProd']
        texto = session['textoBuscarProd']
        tipoBusqueda = listaBusquedaProductos[campoBuscar][1]

        if len(texto) > 0:
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosProductos))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosProductos))
        else:
            listRta = list(db.datosProductos)

        if len(listRta) > 0:
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, data=listRta, title="Productos", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)
        else:
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, title="Productos", usuario=usuario,infoUser = (usuario+" - "+tipoUsuario), opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect("/productos")


@appDash.server.route('/eliminarProducto', methods=('GET','POST'))
def eliminarProducto():
    global opcionesProductos, cabeceraProd
  
    if "usuario" in session and request.method == 'POST':
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        idProducto= request.form['idProducto']
        sino= request.form['sino']

        if sino == "Si":
            rta = db.eliminarProducto(idProducto)
            
            if rta == 1:
                miFlash("Registro Eliminado")
            else:
                miFlash("Registro NO encontrado")

        # cargar datos de busqueda desde las cookies.
        campoBuscar = session['campoBuscarProd']
        texto = session['textoBuscarProd']
        tipoBusqueda = listaBusquedaProductos[campoBuscar][1]

        if len(texto) > 0:
            if tipoBusqueda == "==":
                listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosProductos))
            else:
                listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosProductos))
        else:
            listRta = list(db.datosProductos)

        if len(listRta) > 0:
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, data=listRta, title="Productos", usuario=usuario, opcMenu=opcMenu)
        else:
            opciones = opcBusquedaHTML(listaBusquedaProductos, campoBuscar)
            rtaHTML = render_template("Productos.html", headings=cabeceraProd, opcBusqueda=opciones, title="Productos", usuario=usuario, opcMenu=opcMenu)

        return rtaHTML

    else:
        return redirect("/productos")


@appDash.server.route('/dashboard', methods=('GET',))
def dashboard():
    #print("entro a /dashboard")
    if "usuario" in session and "ver" in db.permisosUsuario["Dashboard"]:
        # Si inicio sesion y tiene permiso, lo lleva a la opcion correspondiente.
        usuario = session['usuario']
        tipoUsuario = session['tipoUsuario']
        db.fijar_permisosUsuario(tipoUsuario)
        opcMenu = opcMenuHTML(db.permisosUsuario)
        dashboard_principal(tipoUsuario, usuario, infoUser = (usuario+" - "+tipoUsuario), opcMenu = opcMenu)
        return appDash.index()

    elif "usuario" in session:
        # Si inicio sesion, pero no tiene permiso, lo lleva a la opcion correspondiente.
        return redirect("/inicio")

    else:
        # No inicio sesion
        return redirect("/index")


# if __name__=='__main__':
#    appDash.run(debug=True)


## cambio en buscarproductos
        # if len(texto) > 0:
        #     """
        #     if tipoBusqueda == "==":
        #         listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosUsuarios))
        #     else:
        #         listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosUsuarios))
        #     """
        #     listRta = crud.consultar_usuarios(campoBuscar, texto)
        # else:
        #     #listRta = list(db.datosUsuarios)
        #     listRta = crud.consultar_usuarios()
        #     # listRta es un arreglo de diccionarios extraidos de db.datosUsuarios
        #     #print("listRta:",listRta)

        # else:
        #     #listRta = list(db.datosUsuarios)
        #     listRta = crud.consultar_usuarios()
        ##


## cambio en modificarproductos

        # ##
        # ## inicia nuevo
        # proveedor = crud.Proveedor(datosProveedor)
        # datosProveedor.pop("idProveedor")
        

        # if proveedor.idProveedor == 0:
        #     # Registro nuevo
        #     rta = crud.insertar_proveedor(datosProveedor)
        #     print("rta :",rta)
        #     if rta > 0:
        #         miFlash("Se inserto un registro")
        #     else:
        #         miFlash("Fallo la creacion del registro")
        #     #print("rta.insert:",rta)
        # else:
        #     rta = crud.actualizar_proveedor(proveedor.idProveedor, datosProveedor)
        #     if rta == 1:
        #         miFlash("Registro Actualizado")
        #     else:
        #         miFlash("Fallo la actualización del registro")
        #     #print("rta.update:",rta)

        # # cargar datos de busqueda desde las cookies.
        # if 'campoBuscarProv' in session:
        #     campoBuscar = session['campoBuscarProv']
        #     texto = session['textoBuscarProv']
        #     tipoBusqueda = listaBusquedaProveedores[campoBuscar][1]
        # else:
        #     campoBuscar = "nombre"
        #     texto = datosProveedor['nombre']
        #     tipoBusqueda = "=="
        # ## fin nuevo ##

        # if len(texto) > 0:
        #     """
        #     if tipoBusqueda == "==":
        #         listRta = list(filter(lambda item: item[campoBuscar].upper() == texto, db.datosUsuarios))
        #     else:
        #         listRta = list(filter(lambda item: texto in item[campoBuscar].upper(), db.datosUsuarios))
        #     """
        #     listRta = crud.consultar_proveedores(campoBuscar, texto)
        # else:
        #     #listRta = list(db.datosUsuarios)
        #     listRta = crud.consultar_proveedores()
