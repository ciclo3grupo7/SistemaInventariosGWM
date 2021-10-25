from SistemaInventarios.modelsDB import *

#CRUD USUARIOS

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

def consultar_usuarios(campoBuscar="", valor=""):
    #print("entro consultar_usuario: ", campoBuscar, valor)
    query = []
    if len(campoBuscar) == 0:
        query = list(Usuarios.select().dicts())
    if campoBuscar == "idUsuario":
        query = list(Usuarios.select().where(Usuarios.idUsuario == valor).dicts())
    elif campoBuscar == "usuario":
        query = list(Usuarios.select().where(Usuarios.usuario == valor).dicts())
    elif campoBuscar == "nombre":
        query = list(Usuarios.select().where(Usuarios.nombre == valor).dicts())
    elif campoBuscar == "tipoUsuario":
        query = list(Usuarios.select().where(Usuarios.tipoUsuario == valor).dicts())
    elif campoBuscar == "estado":
        query = list(Usuarios.select().where(Usuarios.estado == valor).dicts())
    return query

def consultar_usuario(idUsuario=-1, usuario=""):
    #print("entro consultar_usuario: ", idUsuario)
    if idUsuario != -1:
        datosUsuario = list(Usuarios.select().where(Usuarios.idUsuario == idUsuario).dicts())
        usuario = Usuario(datosUsuario[0])
    elif len(usuario) > 0:
        datosUsuario = list(Usuarios.select().where(Usuarios.usuario == usuario).dicts())
        usuario = Usuario(datosUsuario[0])
    else:
        usuario = None
    return usuario

def insertar_usuario(datosUsuario):
    #print("insertar_usuario datosUsuario:",datosUsuario)
    try:
        rta = Usuarios.insert(**datosUsuario).execute()
    except:
        rta = 0
    return rta
    
def actualizar_usuario(idUsuario, datosUsuario):
    try:
        rta = Usuarios.update(**datosUsuario).where(Usuarios.idUsuario == idUsuario).execute()
    except:
        rta = 0
    return rta

def eliminar_usuario(idUsuario):
    try:
        rta = Usuarios.delete().where(Usuarios.idUsuario == idUsuario).execute()
    except:
        rta = 0
    return rta

# CRUD PROVEEDORES

class Proveedor():
    def __init__(self, datosProveedor):
      self.idProveedor = datosProveedor['idProveedor']
      self.nit = datosProveedor['nit']
      self.nombre = datosProveedor['nombre']
      self.direccion = datosProveedor['direccion']
      self.telefono = datosProveedor['telefono']
      self.email = datosProveedor['email']
      self.estado = datosProveedor['estado']
      
      
    def __enter__(self):
      pass
    def __exit__(self, type, val, tb):
      pass

def consultar_proveedores(campoBuscar="", valor=""):
    #print("entro consultar_usuario: ", campoBuscar, valor)
    query = []
    if len(campoBuscar) == 0:
        query = list(Proveedores.select().dicts())
    if campoBuscar == "idProveedor":
        query = list(Proveedores.select().where(Proveedores.idProveedor == valor).dicts())
    elif campoBuscar == "nit":
        query = list(Proveedores.select().where(Proveedores.nit == valor).dicts())
    elif campoBuscar == "Razon Social":
        query = list(Proveedores.select().where(Proveedores.razonSocial == valor).dicts())
    elif campoBuscar == "direccion":
        query = list(Proveedores.select().where(Proveedores.direccion == valor).dicts())
    elif campoBuscar == "telefono":
        query = list(Proveedores.select().where(Proveedores.telefono == valor).dicts())
    elif campoBuscar == "estado":
        query = list(Proveedores.select().where(Proveedores.estado == valor).dicts())
    return query

def consultar_proveedor(idProveedor):
    #print("entro consultar_proveedor: ", idProveedor)
    #print("esta aqui")
    datosProveedor = list(Proveedores.select().where(Proveedores.idProveedor == idProveedor).dicts())
    #print("datosProveedor[0]:",datosProveedor[0])
    proveedor = Proveedor(datosProveedor[0])
    #print("proveedor:",proveedor)
    return proveedor

def insertar_proveedor(datosProveedor):
    #print("insertar_proveedor datosProveedor:",datosProveedor)
    try:
        rta = Proveedores.insert(**datosProveedor).execute()
    except:
        rta = 0
    return rta
    
def actualizar_proveedor(idProveedor, datosProveedor):
    try:
        rta = Proveedores.update(**datosProveedor).where(Proveedores.idProveedor == idProveedor).execute()
    except:
        rta = 0
    return rta

def eliminar_Proveedor(idProveedor):
    try:
        rta = Proveedores.delete().where(Proveedores.idProveedor == idProveedor).execute()
    except:
        rta = 0
    return rta


#CRUD PRODUCTOS

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

def consultar_productos(campoBuscar="", valor=""):
    #print("entro consultar_producto: ", campoBuscar, valor)
    query = []
    if len(campoBuscar) == 0:
        query = list(Productos.select().dicts())
    if campoBuscar == "idProducto":
        query = list(Productos.select().where(Productos.idProducto == valor).dicts())
    elif campoBuscar == "codigo":
        query = list(Productos.select().where(Productos.codigo == valor).dicts())
    elif campoBuscar == "nombreProducto":
        query = list(Productos.select().where(Productos.nombreProducto == valor).dicts())
    elif campoBuscar == "cantMin":
        query = list(Productos.select().where(Productos.cantMin == valor).dicts())
    elif campoBuscar == "cantDispo":
        query = list(Productos.select().where(Productos.cantDispo == valor).dicts())
    elif campoBuscar == "estado":
        query = list(Productos.select().where(Productos.estado == valor).dicts())
    return query

def consultar_producto(idProducto):
    #print("entro consultar_producto: ", idProducto)
    #print("esta aqui")
    datosProducto = list(Productos.select().where(Productos.idProducto == idProducto).dicts())
    #print("datosProducto[0]:",datosProducto[0])
    producto = Productos(datosProducto[0])
    #print("producto:",producto)
    return producto

def insertar_producto(datosProducto):
    #print("insertar_producto datosProducto:",datosProducto)
    try:
        rta = Productos.insert(**datosProducto).execute()
    except:
        rta = 0
    return rta
    
def actualizar_producto(idProducto, datosProducto):
    try:
        rta = Productos.update(**datosProducto).where(Productos.idProducto == idProducto).execute()
    except:
        rta = 0
    return rta

def eliminar_producto(idProducto):
    try:
        rta = Productos.delete().where(Productos.idProducto == idProducto).execute()
    except:
        rta = 0
    return rta

