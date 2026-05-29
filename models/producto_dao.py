from models.database import Database
from models.producto import Producto

class ProductoDAO:
    @staticmethod
    def obtener_todos():
        productos = []
        with Database.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, clave, nombre, costo, precio, cantidad, imagen FROM producto")
            for row in cursor.fetchall():
                prod = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                productos.append(prod.to_dict())
        return productos

    @staticmethod
    def insertar(producto: Producto):
        with Database.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO producto (clave, nombre, costo, precio, cantidad, imagen) VALUES (?, ?, ?, ?, ?, ?)",
                (producto.clave, producto.nombre, producto.costo, producto.precio, producto.cantidad, producto.imagen)
            )
            conn.commit()

    @staticmethod
    def actualizar(producto: Producto):
        with Database.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE producto SET clave=?, nombre=?, costo=?, precio=?, cantidad=?, imagen=? WHERE id=?",
                (producto.clave, producto.nombre, producto.costo, producto.precio, producto.cantidad, producto.imagen, producto.id)
            )
            conn.commit()

    @staticmethod
    def eliminar(id_prod):
        with Database.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM producto WHERE id = ?", (id_prod,))
            conn.commit()