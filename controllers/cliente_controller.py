from models.cliente_dao import ClienteDAO
from models.cliente import Cliente

class ClienteController:
    def __init__(self):
        self.dao = ClienteDAO()

    def login(self, username, password):
        if not username or not password:
            return False, "Por favor, llena todos los campos."
        
        usuario = self.dao.autenticar(username, password)
        if usuario:
            return True, usuario
        return False, "Usuario o contraseña incorrectos."

    def register(self, username, correo, password):
        if not username or not correo or not password:
            return False, "Por favor, llena todos los campos."
        
        nuevo_cliente = Cliente(None, username, correo, password, "cliente")
        if self.dao.registrar(nuevo_cliente):
            return True, "Registro exitoso. Ahora inicia sesión."
        return False, "El nombre de usuario o correo ya existen."