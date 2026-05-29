import flet as ft

class AdminView(ft.Column):
    def __init__(self, controller, controlador, cambiar_vista):
        super().__init__(expand=True)

        self.controller = controller  # MainController
        self.controlador = controlador  # Diccionario global de datos
        self.cambiar_vista = cambiar_vista

        self.controls = [
            self.top_bar(),

            ft.Container(
                expand=True,
                width=float("inf"),
                alignment=ft.Alignment(0, 0),  # Centro real
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[

                        # TÍTULO
                        ft.Text(
                            "Panel de opciones",
                            size=28,
                            weight="bold",
                            color="black"
                        ),

                        # BOTONES CON NUEVA NAVEGACIÓN
                        self.boton("Ganancias y reportes (IA)", "chat_ia"),
                        self.boton("Clientes/Usuarios", "clientes"),
                        self.boton("Administrar productos", "admin_productos"),
                    ]
                )
            )
        ]

    # TOP BAR CON DRAWER ACTIVADO
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
                            src="xdxdxdxddxd.jpg",
                            fit="cover"
                        )
                    )
                ]
            )
        )

    # BOTÓN REUTILIZABLE
    def boton(self, texto, vista):
        return ft.ElevatedButton(
            texto,
            bgcolor="#ff4081",
            color="white",
            width=260,
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda e: self.cambiar_vista(vista)
        )