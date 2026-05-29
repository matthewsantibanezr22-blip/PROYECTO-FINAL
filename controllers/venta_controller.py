from models.venta_dao import VentaDAO

class VentaController:
    def __init__(self):
        self.dao = VentaDAO()

    def procesar_carrito(self, carrito):
        errores = []
        # Asumimos que tu carrito es una lista de diccionarios, y cada producto tiene un "id"
        for prod in carrito:
            # Mandamos a comprar 1 unidad por cada producto en la lista del carrito
            exito, msj = self.dao.registrar_compra(prod["id"], 1)
            if not exito:
                errores.append(f"{prod['nombre']}: {msj}")

        if errores:
            # Si hubo algún error (ej. falta de stock de algún producto), lo unimos en un texto
            return False, "\n".join(errores)
        
        return True, "¡Compra realizada con éxito!"