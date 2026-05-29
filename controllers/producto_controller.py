from models.producto_dao import ProductoDAO
from models.producto import Producto

class ProductoController:
    def __init__(self):
        self.dao = ProductoDAO()

    def listar_productos(self):
        return self.dao.obtener_todos()

    def registrar_producto(self, clave, nombre, costo, precio, cantidad, imagen):
        nuevo_prod = Producto(clave=clave, nombre=nombre, costo=costo, precio=precio, cantidad=cantidad, imagen=imagen)
        self.dao.insertar(nuevo_prod)

    def modificar_producto(self, id_prod, clave, nombre, costo, precio, cantidad, imagen):
        prod_editado = Producto(id_prod=id_prod, clave=clave, nombre=nombre, costo=costo, precio=precio, cantidad=cantidad, imagen=imagen)
        self.dao.actualizar(prod_editado)

    def borrar_producto(self, id_prod):
        self.dao.eliminar(id_prod)