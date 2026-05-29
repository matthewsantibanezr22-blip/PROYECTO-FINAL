import flet as ft
import sqlite3  # <- Modulito clave para conectar con Matthew y los demás

class ClientesView(ft.Column):
    def __init__(self, controller, controlador, cambiar_vista):
        super().__init__(expand=True)

        self.controller = controller      # Tu MainController
        self.controlador = controlador    # Tu almacén de datos global
        self.cambiar_vista = cambiar_vista

        # Cargamos los componentes en orden: Barra superior, título y la tabla
        self.controls = [
            self.top_bar(),
            
            ft.Container(
                padding=ft.padding.only(left=15, top=10, bottom=5),
                content=ft.Text("Lista de Clientes", size=24, weight="bold", color="black")
            ),
            
            self.tabla_clientes()
        ]

    # BARRA SUPERIOR (Homologada con tus otras vistas)
    def top_bar(self):
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.MENU,
                        icon_color="#ff4081",
                        on_click=lambda e: self.controller.abrir_drawer()
                    ),
                    ft.Container(
                        width=40,
                        height=40,
                        border_radius=20,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Image(
                            src="xdxdxdxddxd.jpg",  # <- Asegúrate de que esta foto esté en tu carpeta raíz
                            fit="cover"
                        ),
                        on_click=lambda e: self.controller.accion_perfil()
                    )
                ]
            )
        )

    # GENERACIÓN DE LA TABLA CON DETECTOR DE ERRORES REALES
    def tabla_clientes(self):
        filas = []
        
        try:
            # 🔴 ¡OJO AQUÍ, BRO! 🔴 
            # Cambia "tu_base_de_datos.db" por el nombre real de tu archivo SQLite (ej. "sistema.db", "datos.db")
            conexion = sqlite3.connect("three_cakes.db") 
            cursor = conexion.cursor()
            
            # 🔴 ¡OJO AQUÍ TAMBIÉN! 🔴
            # Cambia "usuarios" por el nombre exacto de la tabla donde guardas los registros de los clientes
            cursor.execute("SELECT username, correo, password FROM usuario") 
            registros = cursor.fetchall()
            conexion.close()

            # Si todo sale bien, procesamos cada fila de la BD
            for registro in registros:
                filas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(registro[0]))), # Nombre
                            ft.DataCell(ft.Text(str(registro[1]))), # Correo
                            ft.DataCell(ft.Text(str(registro[2]))), # Contraseña
                        ]
                    )
                )
                
        except Exception as e:
            # Si algo falla, el "chismoso" atrapa el error y te lo escribe en la pantalla en letras rojas
            error_msg = str(e)
            print(f"ERROR DIRECTO DE BD: {error_msg}") 
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Error de BD", color="red", weight="bold")),
                        ft.DataCell(ft.Text(error_msg, color="red")), # Aquí verás qué falló exactamente
                        ft.DataCell(ft.Text("---")),
                    ]
                )
            )

        # Configuramos la estructura visual de la tabla
        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre", color="#ff4081", weight="bold")),
                ft.DataColumn(ft.Text("Correo Electrónico", color="#ff4081", weight="bold")),
                ft.DataColumn(ft.Text("Contraseña", color="#ff4081", weight="bold")),
            ],
            rows=filas,
            border=ft.border.all(1, "#eeeeee"),
            border_radius=15,
            vertical_lines=ft.border.BorderSide(1, "#eeeeee"),
            horizontal_lines=ft.border.BorderSide(1, "#eeeeee"),
            heading_row_color="#fcfcfc"
        )

        # Retornamos el contenedor con el doble Scroll funcional para móvil
        return ft.Container(
            expand=True,
            padding=10,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO, # Desplazamiento Vertical
                expand=True,
                controls=[
                    ft.Row(
                        scroll=ft.ScrollMode.AUTO, # Desplazamiento Horizontal
                        controls=[tabla]
                    )
                ]
            )
        )