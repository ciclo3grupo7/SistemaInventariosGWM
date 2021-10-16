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
    },
    {
        "cedula": "333333",
        "idUsuario": "3",
        "usuario": "jserge",
        "nombre": "Jose Serge",
        "apellidos": "Serge",
        "email": "m3@d3.com",
        "direccion": "Calle 33",
        "tipoUsuario": "UsuarioFinal",
        "estado": "Activo",
        "clave": "1234",
        "cambiarClave": "0",
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
        "cambiarClave": "1",
    },
]


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
