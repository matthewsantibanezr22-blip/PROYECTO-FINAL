import sqlite3
from models.database import Database
from models.cliente import Cliente

class ClienteDAO:
    def registrar(self, cliente):
        try:
            with Database.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO usuario (username, correo, password, rol) VALUES (?, ?, ?, ?)",
                    (cliente.username, cliente.correo, cliente.password, cliente.rol)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False # El username o el correo ya están ocupados

    def autenticar(self, username, password):
        with Database.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM usuario WHERE username = ? AND password = ?",
                (username, password)
            )
            row = cursor.fetchone()
            if row:
                # row = (id, username, correo, password, rol)
                return Cliente(*row)
            return None