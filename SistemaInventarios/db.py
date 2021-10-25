datosUsuarios = [
    {
        "idUsuario": "1",
        "cedula": "111111",
        "usuario": "yperez",
        "nombre": "Yolima Perez",
        # "apellido": "Perez",
        "email": "m1@d1.com",
        "direccion": "Calle 11",
        "tipoUsuario": "Administrador",
        "estado": "Activo",
        "clave": "1234",
        "cambiarClave": "0",
        "aceptarPolitica":0,
    },
    {
        "cedula": "222222",
        "idUsuario": "2",
        "usuario": "crojas",
        "nombre": "Camila Rojas",
        #"apellido": "Rojas",
        "email": "m2@d2.com",
        "direccion": "Calle 22",
        "tipoUsuario": "SuperAdministrador",
        "estado": "Activo",
        "clave": "1234",
        "cambiarClave": "0",
        "aceptarPolitica":0,
    },
    {
        "cedula": "333333",
        "idUsuario": "3",
        "usuario": "jserge",
        "nombre": "Jose Serge",
        "apellidos": "Serge",
        "email": "m3@d3.com",
        "direccion": "Calle 33",
        "tipoUsuario": "SuperAdministrador",
        "estado": "Activo",
        "clave": "1234",
        "cambiarClave": "0",
        "aceptarPolitica":0,
    },
    {
        "idUsuario": "4",
        "cedula": "444444",
        "usuario": "rmillan",
        "nombre": "Ricardo Millan",
        # "apellidos": "Millan",
        "email": "m4@d4.com",
        "direccion": "Calle 44",
        "tipoUsuario": "Administrador",
        "estado": "Activo",
        "clave": "1234",
        "cambiarClave": "0",
        "aceptarPolitica":1,
    },
    {
        "idUsuario": "5",
        "cedula": "555555",
        "usuario": "jmunoz",
        "nombre": "Jorge Muñoz",
        # "apellidos": "Muñoz",
        "email": "m5@d5.com",
        "direccion": "Calle 55",
        "tipoUsuario": "UsuarioFinal",
        "estado": "Activo",
        "clave": "1234",
        "cambiarClave": "0",
        "aceptarPolitica":0,
    },
    {
        "idUsuario": "6",
        "cedula": "555555",
        "usuario": "otro",
        "nombre": "Otro Usuario",
        # "apellidos": "Muñoz",
        "email": "m5@d5.com",
        "direccion": "Calle 66",
        "tipoUsuario": "UsuarioFinal",
        "estado": "Inactivo",
        "clave": "1234",
        "cambiarClave": "0",
        "aceptarPolitica":0,
    },
]

permisosUsuario = {}

maxIdUsuario = 6

class Usuario():
    def __init__(self, datosUsuario):
      self.idUsuario = datosUsuario['idUsuario']
      self.cedula = datosUsuario['cedula']
      self.usuario = datosUsuario['usuario']
      self.nombre = datosUsuario['nombre']
      #self.apellido = datosUsuario['apellido']
      self.email = datosUsuario['email']
      self.direccion = datosUsuario['direccion']
      self.tipoUsuario = datosUsuario['tipoUsuario']
      self.estado = datosUsuario['estado']
      self.clave = datosUsuario['clave']
      self.cambiarClave = datosUsuario['cambiarClave']
    def __enter__(self):
      pass
    def __exit__(self, type, val, tb):
      pass



def buscarUsuario(idUsuario):
    global datosUsuarios
    rta = list(filter(lambda item: item['idUsuario'] == idUsuario, datosUsuarios))
    if len(rta) > 0:
        u = Usuario(rta[0])
        #print("u.idUsuario: ", u.idUsuario)
    else:
        u = None
    return(u)


def actualizarUsuario(usuario):
    global datosUsuarios
    iPos = next((i for i, x in enumerate(datosUsuarios) if x["idUsuario"] == usuario.idUsuario), None)
    datosUsuario = {
            "idUsuario": usuario.idUsuario,
            "cedula": usuario.cedula,
            "usuario": usuario.usuario,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "direccion": usuario.direccion,
            #"apellido": usuario.apellido,
            "tipoUsuario": usuario.tipoUsuario,
            "estado": usuario.estado,
            "clave": usuario.clave,
            "cambiarClave": usuario.cambiarClave,
        }
    if iPos == None:
        # Registro nuevo
        datosUsuarios.append(datosUsuario)
        return(1)
    else:
        # Registro actualizado
        datosUsuarios[iPos] = datosUsuario
        return(2)


def eliminarUsuario(idUsuario):
    global datosUsuarios
    iPos = next((i for i, x in enumerate(datosUsuarios) if x["idUsuario"] == idUsuario), None)
    if iPos == None:
        # Registro no encontrado
        return(0)
    else:
        # Registro eliminado
        del datosUsuarios[iPos]
        return(1)

#Proveedores RJMM

datosProveedores = [
    {
        "idProveedor": "1",
        "nit": "1111",
        "nombre": "Proveedor 1",
        "direccion": "Call 43",
        "telefono": "2233",
        "email": "s@g.com",
        "estado": "Activo"
    },
    {
        "idProveedor": "2",
        "nit": "2222",
        "nombre": "Proveedor 2",
        "direccion": "Call 100",
        "telefono": "4455",
        "email": "s2@g2.com",
        "estado": "Activo"
    },
    {
        "idProveedor": "3",
        "nit": "3333",
        "nombre": "Proveedor 3",
        "direccion": "Av. 68",
        "telefono": "6677",
        "email": "s3@g3.com",
        "estado": "Activo"
    },
]

maxIdProveedor = 3

class Proveedor():
    def __init__(self, datosProveedor):
      self.idProveedor = datosProveedor['idProveedor']
      self.nit = datosProveedor['nit']
      self.nombre = datosProveedor['nombre']
      self.direccion = datosProveedor['direccion']
      #self.apellido = datosUsuario['apellido']
      self.telefono = datosProveedor['telefono']
      self.email = datosProveedor['email']
      self.estado = datosProveedor['estado']
      
    def __enter__(self):
      pass
    def __exit__(self, type, val, tb):
      pass

def buscarProveedor(idProveedor):
    global datosProveedores
    rta = list(filter(lambda item: item['idProveedor'] == idProveedor, datosProveedores))
    if len(rta) > 0:
        u = Proveedor(rta[0])
        #print("u.idUsuario: ", u.idUsuario)
    else:
        u = None
    return(u)

def actualizarProveedor(proveedor):
    global datosProveedores
    iPos = next((i for i, x in enumerate(datosProveedores) if x["idProveedor"] == proveedor.idProveedor), None)
    datosProveedor = {
            "idProveedor": proveedor.idProveedor,
            "nit": proveedor.nit,
            "nombre": proveedor.nombre,
            "direccion": proveedor.direccion,
            "telefono": proveedor.telefono,
            "email": proveedor.email,
            #"apellido": usuario.apellido,
            "estado": proveedor.estado,
            
        }
    if iPos == None:
        # Registro nuevo
        datosProveedores.append(datosProveedor)
        return(1)
    else:
        # Registro actualizado
        datosProveedores[iPos] = datosProveedor
        return(2)

def eliminarProveedor(idProveedor):
    global datosProveedores
    iPos = next((i for i, x in enumerate(datosProveedores) if x["idProveedor"] == idProveedor), None)
    if iPos == None:
        # Registro no encontrado
        return(0)
    else:
        # Registro eliminado
        del datosProveedores[iPos]
        return(1)



#productos RJMM


datosProductos = [
    {
        "idProducto": "1",
        "nombre": "Toyota Prado",
        "cantMin": "10",
        "cantBodega": "40",
        "descripcion": "Modelo 2018, automatico",
        "estado": "Activo"
    },
    {
        "idProducto": "2",
        "nombre": "Hyundai Tucson",
        "cantMin": "15",
        "cantBodega": "9",
        "descripcion": "Modelo 2021, mecanico",
        "estado": "Activo"
    },
    {
        "idProducto": "3",
        "nombre": "Mazda 5",
        "cantMin": "15",
        "cantBodega": "9",
        "descripcion": "Modelo 2017, automatico",
        "estado": "Activo"
    },
    {
        "idProducto": "4",
        "nombre": "Kia Picanto",
        "cantMin": "15",
        "cantBodega": "9",
        "descripcion": "Modelo 2020, mecanico",
        "estado": "Inactivo"
    },
]

maxIdProducto = 5

class Producto():
    def __init__(self, datosProducto):
      self.idProducto = datosProducto['idProducto']
      self.codigo = datosProducto['codigo']
      self.nombreProducto = datosProducto['nombreProducto']
      self.cantMin = datosProducto['cantMin']
      self.cantDispo = datosProducto['cantDispo']
      self.estado = datosProducto['estado']
      
    def __enter__(self):
      pass
    def __exit__(self, type, val, tb):
      pass

def buscarProducto(idProducto):
    global datosProductos
    rta = list(filter(lambda item: item['idProducto'] == idProducto, datosProductos))
    if len(rta) > 0:
        u = Producto(rta[0])
        
    else:
        u = None
    return(u)

def actualizarProducto(producto):
    global datosProductos
    iPos = next((i for i, x in enumerate(datosProductos) if x["idProducto"] == producto.idProducto), None)
    datosProducto = {
            "idProducto": producto.idProducto,
            "nombre": producto.nombre,
            "cantMin": producto.cantMin,
            "cantBodega": producto.cantBodega,
            "descripcion": producto.descripcion,
            "estado": producto.estado,
            
        }
    if iPos == None:
        # Registro nuevo
        datosProductos.append(datosProducto)
        return(1)
    else:
        # Registro actualizado
        datosProductos[iPos] = datosProducto
        return(2)

def eliminarProducto(idProducto):
    global datosProductos
    iPos = next((i for i, x in enumerate(datosProductos) if x["idProducto"] == idProducto), None)
    if iPos == None:
        # Registro no encontrado
        return(0)
    else:
        # Registro eliminado
        del datosProductos[iPos]
        return(1)


def fijar_permisosUsuario(tipoUsuario):
    global permisosUsuario
    permisosUsuario = {}
    if tipoUsuario == "UsuarioFinal":
        permisosUsuario = {
            "Usuarios": (""),
            "Proveedores": ("ver","cre", "mod", "eli"),
            "Productos": ("ver","cre", "mod", "eli"),
            "Dashboard": ("ver")
        }
    elif tipoUsuario == "Administrador":
        permisosUsuario = {
            "Usuarios": ("ver","cre", "mod", "eli"),
            "Proveedores": (""),
            "Productos": ("ver"),
            "Dashboard": ("")
        }
    elif tipoUsuario == "SuperAdministrador":
        permisosUsuario = {
            "Usuarios": ("ver","cre", "mod", "eli"),
            "Proveedores": ("ver","cre", "mod", "eli"),
            "Productos": ("ver","cre", "mod", "eli"),
            "Dashboard": ("ver")
        }
    #print(permisosUsuario)



