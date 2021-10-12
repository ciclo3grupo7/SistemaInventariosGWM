from flask import Flask, render_template, redirect, request, flash
import os

app= Flask(__name__)
app.secret_key= os.urandom(32)

datosUsuarios = {
    "Yolima": "1234",
    "Camila": "1234",
    "Jose": "1234",
    "Ricardo": "1234",
    "Jorge": "1234"
}
# Interacción de Proveedores
cabecera = ("Nit","Razón Social","Dirección","Telefono","email","estado","acciones")

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
cabeceraP = ("Identificador","Nombre"," Cantidad Minima","Cantidad Disponible","Descripcion","Estado","acciones")

datosProductos = [(1,"Carro Toyota Prado",2,0,"Modelo 2018, automatico","Activo"),
    (2,"Carro Hyundai Tucson",4,1,"Modelo 2021, mecanico","Activo"),(3,"Carro Mazda 5",2,1,"Modelo 2017 automatico","Activo")]

@app.route('/', methods=['GET'])
def index():
    return redirect("/index")


@app.route('/index', methods=('GET', 'POST'))
def login():
    return render_template("index.html")


@app.route('/validarLogin', methods=('GET', 'POST'))
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


@app.route('/inicio', methods=['GET'])
def inicio():
    return render_template("Inicio.html")

#USUARIOS JMSS
@app.route('/usuarios', methods=('GET','POST'))
def usuarios():
    return render_template("Usuarios.html")


@app.route('/ValidarBusquedaUser', methods=('GET','POST'))
def ValidarBusquedaUser():
    if request.method == 'POST':
        seleccion = request.form['select']
        busqueda = request.form['text']
        existe = 'NO'
        if seleccion == 'usuario':
            #Buscar un Usuario por su respectiva DESCRIPCIÓN (Usuario)
            tam = (len(datosUsuar))
            for i in range(tam):
                if busqueda in datosUsuar[i][0]:
                    data = [(datosUsuar[i][0],datosUsuar[i][1],datosUsuar[i][2],datosUsuar[i][3])]
                    existe = "SI" 

            if existe == 'SI':
                flash("El usuario " + busqueda + " Ya Existe En Nuestra Plataforma")
                return render_template("Usuarios.html",headings=cabeceraUsuar ,data=data)
            else:
                flash("El Usuario "+ busqueda + " No Fue Encontrado")
                return render_template('Usuarios.html')

        if seleccion == 'Identificador':
            #Buscar un Usuario por su respectiva Identificador (Nombre)
            tam = (len(datosUsuar))
            data=[] #limpio la data
            print("tam : ",tam)
            for i in range(tam):
                if (busqueda in datosUsuar[i][1]):
                    existe = "SI"
                    data.append((datosUsuar[i][0],datosUsuar[i][1],datosUsuar[i][2],datosUsuar[i][3]))
                    #
            if existe == 'SI':
                    flash("El usuario Con El Identificador " + busqueda + ", Ya Existe!")
                    return render_template("Usuarios.html",headings=cabeceraUsuar ,data=data)
            else:
                flash("El Usuario Con El Identificador "+ busqueda + ", No Fue Encontrado!")
                return render_template('Usuarios.html')


        if seleccion == 'Perfil':
            #Buscar un Usuario por su respectiva Perfil (Rol)
            data=[]
            tam = (len(datosUsuar))
            for i in range(tam):
                if busqueda in datosUsuar[i][2]:
                    data.append((datosUsuar[i][0],datosUsuar[i][1],datosUsuar[i][2],datosUsuar[i][3]))
                    existe = "SI" 

            if existe == 'SI':
                flash("Datos Encontrados")
                return render_template("Usuarios.html",headings=cabeceraUsuar ,data=data)
            else:
                flash("El Perfil "+ busqueda + " De Usuario, No Fue Encontrado")
                return render_template('Usuarios.html')

        if seleccion == 'Estado':
            tam = (len(datosUsuar))
            data=[] #limpio la data
            for i in range(tam):
                if (busqueda in datosUsuar[i][3]):
                    existe = "SI"
                    data.append((datosUsuar[i][0],datosUsuar[i][1],datosUsuar[i][2],datosUsuar[i][3]))
                    #
            if existe == 'SI':
                flash("Los Perfiles De Estado " + busqueda + " Son: ")
                return render_template("Usuarios.html",headings=cabeceraUsuar ,data=data)
            else:
                flash("Los Perfiles De Estado " + busqueda + " , No Fueron Encontrados!")
                return redirect("/usuarios")


@app.route('/insertarUsuarios', methods=('GET','POST'))
def insertarUsuarios():
    if request.method == 'POST':
        # Entra cuando el llamado es hecho por metodo POST.
        
        cedula = request.form['cedula']
        nombrecomplet = request.form['nombre']
        direccion = request.form['direccion']
        email = request.form['mail']
        perfil = request.form['perfil']
        estado = request.form['estado']
        contraseña = request.form['password']
        
        #Datos para crear un Usuario (Cedula, nombre completo, dirección, email, perfil, estado y contraseña)
        #El Usuario va a ser su Email
        existe = "NO"
        indice = 0
        if existe == "SI":
                flash("Registro Actualizado")
                datosUsuar.pop(indice)
                datosUsuar.append((email,nombrecomplet, perfil,estado))
        else:
            datosUsuar.append((email,nombrecomplet, perfil,estado))
            flash("Se inserto un registro")
            
        return redirect("/usuarios")


#PRODUCTOS PROVEEDORES

@app.route('/proveedores', methods=('GET','POST'))
def proveedores():
    return render_template("Proveedores.html")

@app.route('/buscarProveedores', methods=('GET','POST'))
def buscarproveedores():
    
    if request.method == 'POST':
        #RJMM Entra cuando el llamado es hecho por metodo POST.
        seleccion = request.form['select']
        texto = request.form['text']
        #RJMM Defino variable para que el ciclo se ejecute hasta el fin
        existe="NO"
        
        #RJMM Condicion para determinar busqueda x nit
        if seleccion == "nit":
            #RJMM se tiene en cuenta en caso de agregar, nuevos proveedores
            tam = (len(datosProveedores))
            #RJMM Recorro la data
            for i in range(tam):
                if (datosProveedores[i][0]==texto):
                    #RJMM construyo la data
                    data = [(datosProveedores[i][0],datosProveedores[i][1],datosProveedores[i][2],datosProveedores[i][3],datosProveedores[i][4],datosProveedores[i][5])]
                    existe = "SI"
                    #indice = i
            
            if existe == "SI":
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos Encontrados")
                #RJMM retorno la pagina, pero envio por parametros los valores de la pagina
                #data que necesita
                #return render_template("Proveedores.html",headings=headings,data=[(datosProveedores[indice][0],datosProveedores[indice][1],datosProveedores[indice][2],datosProveedores[indice][3],datosProveedores[indice][4],datosProveedores[indice][5])])
                return render_template("Proveedores.html",headings=cabecera,data=data)
            
            else:
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos No Encontrados")
                return redirect("/proveedores")
        
        #RJMM Condicion para determinar busqueda x nombre de la empresa
        if seleccion == "nombre":
            #RJMM se tiene en cuenta en caso de agregar, nuevos proveedores
            tam = (len(datosProveedores))
            data=[] #limpio la data
            print("tam : ",tam)
            for i in range(tam):
                if (texto in datosProveedores[i][1]):
                    existe = "SI"
                    data.append((datosProveedores[i][0],datosProveedores[i][1],datosProveedores[i][2],datosProveedores[i][3],datosProveedores[i][4],datosProveedores[i][5]))
                    #print("Data :",data)
            if existe == "SI":
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos Encontrados")
                #RJMM retorno la pagina, pero envio por parametros los valores de la pagina
                #data que necesita
                return render_template("Proveedores.html",headings=cabecera,data=data)
            else:
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos No Encontrados")
                return redirect("/proveedores")

        #RJMM Condicion para determinar busqueda x direccion
        if seleccion == "direccion":
            #RJMM se tiene en cuenta en caso de agregar, nuevos proveedores
            tam = (len(datosProveedores))
            data=[] #limpio la data
            for i in range(tam):
                #Busco el texto de acuerdo a la razon social
                if (texto in datosProveedores[i][2]):
                    existe = "SI"
                    data.append((datosProveedores[i][0],datosProveedores[i][1],datosProveedores[i][2],datosProveedores[i][3],datosProveedores[i][4],datosProveedores[i][5]))
                
            if existe == "SI":
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos Encontrados")
                #RJMM retorno la pagina, pero envio por parametros los valores de la pagina
                #data que necesita
                return render_template("Proveedores.html",headings=cabecera,data=data)
            else:
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos No Encontrados")
                return redirect("/proveedores")

        #RJMM Condicion para determinar busqueda x telefono
        if seleccion == "telefono":
            #RJMM se tiene en cuenta en caso de agregar, nuevos proveedores
            tam = (len(datosProveedores))
            data=[] #limpio la data
            for i in range(tam):
                #Busco el texto de acuerdo a la razon social
                if (texto in datosProveedores[i][3]):
                    existe = "SI"
                    data.append((datosProveedores[i][0],datosProveedores[i][1],datosProveedores[i][2],datosProveedores[i][3],datosProveedores[i][4],datosProveedores[i][5]))
                
            if existe == "SI":
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos Encontrados")
                #RJMM retorno la pagina, pero envio por parametros los valores de la pagina
                #data que necesita
                return render_template("Proveedores.html",headings=cabecera,data=data)
            else:
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos No Encontrados")
                return redirect("/proveedores")    

        #RJMM Condicion para determinar busqueda x direccion
        if seleccion == "email":
            #RJMM se tiene en cuenta en caso de agregar, nuevos proveedores
            tam = (len(datosProveedores))
            data=[] #limpio la data
            for i in range(tam):
                #Busco el texto de acuerdo a la razon social
                if (texto in datosProveedores[i][4]):
                    existe = "SI"
                    data.append((datosProveedores[i][0],datosProveedores[i][1],datosProveedores[i][2],datosProveedores[i][3],datosProveedores[i][4],datosProveedores[i][5]))
                
            if existe == "SI":
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos Encontrados")
                #RJMM retorno la pagina, pero envio por parametros los valores de la pagina
                #data que necesita
                return render_template("Proveedores.html",headings=cabecera,data=data)
            else:
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos No Encontrados")
                return redirect("/proveedores")

        #RJMM Condicion para determinar busqueda x direccion
        if seleccion == "estado":
            #RJMM se tiene en cuenta en caso de agregar, nuevos proveedores
            tam = (len(datosProveedores))
            data=[] #limpio la data
            for i in range(tam):
                #Busco el texto de acuerdo a la razon social
                if (datosProveedores[i][5] == texto):
                    existe = "SI"
                    data.append((datosProveedores[i][0],datosProveedores[i][1],datosProveedores[i][2],datosProveedores[i][3],datosProveedores[i][4],datosProveedores[i][5]))
                
            if existe == "SI":
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos Encontrados")
                #RJMM retorno la pagina, pero envio por parametros los valores de la pagina
                #data que necesita
                return render_template("Proveedores.html",headings=cabecera,data=data)
            else:
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos No Encontrados")
                return redirect("/proveedores")    
                   

@app.route('/insertarProveedor', methods=('GET','POST'))
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
                flash("Registro Actualizado")
                datosProveedores.pop(indice)
                datosProveedores.append((nit,razonSocial,direccion, telefono,email,estado))
        else:
            datosProveedores.append((nit,razonSocial,direccion, telefono,email,estado))
            flash("Se inserto un registro")
            
        return redirect("/proveedores")        

#PRODUCTOS LOGICA

@app.route('/productos', methods=('GET','POST'))
def productos():
    return render_template("Productos.html")

@app.route('/buscarProductos', methods=('GET','POST'))
def buscarproductos():

    if request.method == 'POST':
        #RJMM Entra cuando el llamado es hecho por metodo POST.
        seleccion = request.form['select']
        texto = request.form['text']
        #RJMM Defino variable para que el ciclo se ejecute hasta el fin
        existe="NO"
        
        #RJMM Condicion para determinar busqueda x nit
        if seleccion == "id":
            #RJMM se tiene en cuenta en caso de agregar, nuevos proveedores
            tam = (len(datosProductos))
            #RJMM Recorro la data
            for i in range(tam):
                if (datosProductos[i][0]==int(texto)):
                    #RJMM construyo la data
                    data = [(datosProductos[i][0],datosProductos[i][1],datosProductos[i][2],datosProductos[i][3],datosProductos[i][4],datosProductos[i][5])]
                    existe = "SI"
                    #indice = i
            
            if existe == "SI":
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos Encontrados")
                #RJMM retorno la pagina, pero envio por parametros los valores de la pagina
                #data que necesita
                #return render_template("Proveedores.html",headings=headings,data=[(datosProveedores[indice][0],datosProveedores[indice][1],datosProveedores[indice][2],datosProveedores[indice][3],datosProveedores[indice][4],datosProveedores[indice][5])])
                return render_template("Productos.html",headings=cabeceraP,data=data)
            
            else:
                #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos No Encontrados")
                return redirect("/productos")
        
        if seleccion == "nombre": #RJMM se tiene en cuenta en caso de agregar, nuevos proveedores
            tam = (len(datosProductos))
            data=[] #limpio la data
            print("tam : ",tam)

            for i in range(tam):
                if (texto in datosProductos[i][1]):
                    existe = "SI"
                    data.append((datosProductos[i][0],datosProductos[i][1],datosProductos[i][2],datosProductos[i][3],datosProductos[i][4],datosProductos[i][5]))

            if existe == "SI": #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos Encontrados")               
                return render_template("Productos.html",headings=cabeceraP,data=data)  #RJMM retorno la pagina, pero envio por parametros los valores de la pagina
            else:  #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos No Encontrados")
                return redirect("/productos")

        if seleccion == "descripcion":
            tam = (len(datosProductos))
            data=[] #limpio la data
            print("tam : ",tam)
            for i in range(tam):
                if (texto in datosProductos[i][4]):
                    existe = "SI"
                    data.append((datosProductos[i][0],datosProductos[i][1],datosProductos[i][2],datosProductos[i][3],datosProductos[i][4],datosProductos[i][5]))
            if existe == "SI": #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos Encontrados")
                return render_template("Productos.html",headings=cabeceraP,data=data)
            else:  #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos No Encontrados")
                return redirect("/productos")

        if seleccion == "estado":  #RJMM se tiene en cuenta en caso de agregar, nuevos proveedores
            tam = (len(datosProductos))
            data=[] #limpio la data
            for i in range(tam):  #RJMM Recorro la data
                if (datosProductos[i][5] == texto):
                    existe = "SI"
                    data.append((datosProductos[i][0],datosProductos[i][1],datosProductos[i][2],datosProductos[i][3],datosProductos[i][4],datosProductos[i][5]))
            
            if existe == "SI": #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos Encontrados")
                return render_template("Productos.html",headings=cabeceraP,data=data)
            
            else: #RJMM Mensaje flash, muestra si el dato se encontro
                flash("Datos No Encontrados")
                return redirect("/productos")

#metodo insertar producto
@app.route('/insertarProducto', methods=('GET','POST'))
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
                flash("Registro Actualizado")
                datosProductos.pop(indice)
                datosProductos.append((int(codigo),nombre,int(cantidadMinima),int(cantidadDisponible),descripcion,estado))
        else:
            datosProductos.append((int(codigo),nombre,int(cantidadMinima),int(cantidadDisponible),descripcion,estado))
            flash("Se inserto un registro")
            
        return redirect("/productos") 


@app.route('/dashboard', methods=['GET'])
def dashBoard():
    return render_template("DashBoard.html")


if __name__=='__main__':
    app.run(debug=True)

