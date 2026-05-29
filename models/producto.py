class Producto:
    # CORREGIDO: Agregamos 'costo=0.0' en la firma de la función en la posición correcta
    def __init__(self, id_prod=None, clave="", nombre="", costo=0.0, precio=0.0, cantidad=0, imagen=""):
        self.id = id_prod
        self.clave = clave
        self.nombre = nombre
        self.costo = costo  # CORREGIDO: Ahora sí guarda el costo real que le pases
        self.precio = precio
        self.cantidad = cantidad
        self.imagen = imagen

    def to_dict(self):
        return {
            "id": self.id,
            "clave": self.clave,
            "nombre": self.nombre,
            "costo": self.costo,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "imagen": self.imagen
        }