import sqlite3

class Database:
    @staticmethod
    def conectar():
        return sqlite3.connect("three_cakes.db")

    @staticmethod
    def inicializar_db():
        with Database.conectar() as conn:
            cursor = conn.cursor()
            
            # 1. Tabla Producto
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS producto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clave TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    costo REAL NOT NULL,
                    precio REAL NOT NULL,
                    cantidad INTEGER NOT NULL,
                    imagen TEXT NOT NULL
                )
            """)
            
            # 2. Tabla Cliente/Usuario
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    correo TEXT UNIQUE, 
                    password TEXT NOT NULL,
                    rol TEXT NOT NULL
                )
            """)
            
            # 3. 🔥 NUEVA TABLA: Historial de Ventas para la IA
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS venta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER,
                    nombre_producto TEXT NOT NULL,
                    cantidad_vendida INTEGER NOT NULL,
                    costo_fabricacion REAL NOT NULL,
                    precio_venta REAL NOT NULL,
                    ganancia_total REAL NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(producto_id) REFERENCES producto(id) ON DELETE SET NULL
                )
            """)
            
            # Insertar Administrador por defecto si la tabla está vacía
            cursor.execute("SELECT * FROM usuario WHERE username = 'admin'")
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO usuario (username, correo, password, rol) VALUES (?, ?, ?, ?)",
                    ("admin", "admin@threecakes.com", "admin123", "administrador")
                )
            
            conn.commit()