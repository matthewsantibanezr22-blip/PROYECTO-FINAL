import sqlite3
from models.database import Database

class VentaDAO:
    @staticmethod
    def registrar_compra(producto_id, cantidad_a_comprar):
        conn = Database.conectar()
        cursor = conn.cursor()
        try:
            # 1. Verificar si hay stock suficiente del producto
            cursor.execute("SELECT nombre, costo, precio, cantidad FROM producto WHERE id = ?", (producto_id,))
            prod = cursor.fetchone()
            
            if not prod:
                return False, "El producto no existe."
            
            nombre, costo, precio, stock_actual = prod
            
            if stock_actual < cantidad_a_comprar:
                return False, f"Stock insuficiente. Solo quedan {stock_actual} unidades."
            
            # 2. Restar el stock en la tabla producto
            nuevo_stock = stock_actual - cantidad_a_comprar
            cursor.execute("UPDATE producto SET cantidad = ? WHERE id = ?", (nuevo_stock, producto_id))
            
            # 3. Calcular las finanzas de esta venta
            costo_total_fab = costo * cantidad_a_comprar
            ingreso_total = precio * cantidad_a_comprar
            ganancia_neta = ingreso_total - costo_total_fab
            
            # 4. Guardar en el historial de ventas para la IA
            cursor.execute("""
                INSERT INTO venta (producto_id, nombre_producto, cantidad_vendida, costo_fabricacion, precio_venta, ganancia_total)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (producto_id, nombre, cantidad_a_comprar, costo_total_fab, ingreso_total, ganancia_neta))
            
            conn.commit()
            return True, "Compra realizada con éxito y stock actualizado."
            
        except sqlite3.Error as e:
            conn.rollback()
            return False, f"Error en la base de datos: {str(e)}"
        finally:
            conn.close()

    @staticmethod
    def obtener_todas_las_ventas():
        """Este método lo va a usar la IA para leer todo el historial en bruto"""
        conn = Database.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre_producto, cantidad_vendida, costo_fabricacion, precio_venta, ganancia_total, fecha FROM venta")
        ventas = cursor.fetchall()
        conn.close()
        return ventas