import flet as ft

class HomeView(ft.Column):
    def __init__(self, controller, controlador, cambiar_vista):
        super().__init__(expand=True, spacing=10)

        self.controller = controller
        self.controlador = controlador
        self.cambiar_vista = cambiar_vista

        self.grid = ft.GridView(
            expand=True,
            runs_count=2,
            spacing=10,
            run_spacing=10,
            padding=10,
            child_aspect_ratio=0.87
        )

        self.txt_buscar = ft.TextField(
            hint_text="Buscar...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=20,
            filled=True,
            bgcolor="#eeeeee",
            expand=True,
            on_change=self.filtrar_productos
        )

        # 🔥 Se cargan los productos pero le decimos a Flet que no actualice la app todavía
        self.cargar_productos(self.controlador["productos"], actualizar=False)

        self.controls = [
            self.top_bar(),
            self.header(),
            self.buscador(),
            ft.Container(
                expand=True,
                content=self.grid
            )
        ]

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
                        content=ft.Image(src="xdxdxdxddxd.jpg", fit="cover"),
                        on_click=lambda e: self.controller.accion_perfil()
                    )
                ]
            )
        )

    def header(self):
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=10),
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Text("Encuentra el mejor", size=29, weight="bold", color="#ff4081"),
                    ft.Text("postre para ti.", size=29, weight="bold", color="#ff4081"),
                ]
            )
        )

    def buscador(self):
        return ft.Container(
            padding=ft.padding.only(left=10, right=10, top=10),
            content=self.txt_buscar
        )

    def filtrar_productos(self, e):
        texto = self.txt_buscar.value.lower()
        filtrados = [p for p in self.controlador["productos"] if texto in p["nombre"].lower()]
        # Aquí la app ya arrancó, entonces SÍ actualizamos visualmente
        self.cargar_productos(filtrados, actualizar=True)

    def cargar_productos(self, lista, actualizar=True):
        self.grid.controls.clear()
        
        for producto in lista:
            self.grid.controls.append(self.crear_tarjeta(producto))
        
        # 🔥 Candado de seguridad para evitar errores al arrancar
        if actualizar and self.page:
            self.update()

    def crear_tarjeta(self, producto):
        return ft.Container(
            bgcolor="#b4b4b4",
            border_radius=15,
            padding=10,
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Container(
                        border_radius=15,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Image(
                            src=producto["imagen"],
                            height=100,
                            fit="cover"
                        )
                    ),
                    ft.Text(producto["nombre"], color="white", weight="bold"),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(f"${producto['precio']}", color="#ff4081", weight="bold"),
                            ft.Row(
                                spacing=2,
                                controls=[
                                    ft.Icon(ft.Icons.STAR, color="yellow", size=16),
                                    ft.Icon(ft.Icons.STAR, color="yellow", size=16),
                                    ft.Icon(ft.Icons.STAR, color="yellow", size=16),
                                    ft.Icon(ft.Icons.STAR, color="yellow", size=16),
                                    ft.Icon(ft.Icons.STAR_HALF, color="yellow", size=16),
                                ]
                            )
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.FAVORITE, 
                                icon_color="#e11414", 
                                icon_size=18,
                                on_click=lambda e, p=producto: self.agregar_favorito(p)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.SHOPPING_BAG, 
                                icon_color="#11c66f", 
                                icon_size=18,
                                on_click=lambda e, p=producto: self.agregar_carrito(p)
                            ),
                        ]
                    )
                ]
            )
        )

    def abrir_producto(self, producto):
        dialog = ft.AlertDialog(
            title=ft.Text(producto["nombre"]),
            content=ft.Column([
                ft.Image(src=producto["imagen"]),
                ft.Text(f"${producto['precio']}")
            ], compact=True),
            actions=[
                ft.TextButton("Favorito", on_click=lambda e: [self.agregar_favorito(producto), self.cerrar_dialog()]),
                ft.TextButton("Agregar al carrito", on_click=lambda e: [self.agregar_carrito(producto), self.cerrar_dialog()])
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def cerrar_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def agregar_favorito(self, producto):
        if producto not in self.controlador["favoritos"]:
            self.controlador["favoritos"].append(producto)

    def agregar_carrito(self, producto):
        self.controlador["carrito"].append(producto)