import flet as ft

class AdminProductosView(ft.Column):
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
            child_aspect_ratio=0.55 
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

        # 🔥 Cargamos en silencio sin forzar error de la página
        self.cargar_productos(self.controlador["productos"], actualizar=False)

        self.controls = [
            self.top_bar(),
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

    def buscador(self):
        return ft.Container(
            padding=ft.padding.only(left=10, right=10, top=10),
            content=self.txt_buscar
        )

    def filtrar_productos(self, e):
        texto = self.txt_buscar.value.lower()
        filtrados = [p for p in self.controlador["productos"] if texto in p["nombre"].lower()]
        self.cargar_productos(filtrados, actualizar=True)

    def cargar_productos(self, lista, actualizar=True):
        self.grid.controls.clear()
        
        for producto in lista:
            self.grid.controls.append(self.crear_tarjeta_admin(producto))

        # La tarjeta de Agregar Producto siempre se queda anclada al final
        self.grid.controls.append(
            ft.Container(
                bgcolor="#9cc7df",
                border_radius=15,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.ADD, size=40, color="white"),
                        ft.Text("Agregar Producto", color="white", weight="bold", size=12)
                    ]
                ),
                on_click=lambda e: self.cambiar_vista("agregar_producto")
            )
        )

        if actualizar and self.page:
            self.update()

    def crear_tarjeta_admin(self, producto):
        return ft.Container(
            bgcolor="#b4b4b4",
            border_radius=15,
            padding=10,
            content=ft.Column(
                spacing=4, 
                controls=[
                    ft.Image(src=producto["imagen"], height=95, fit="cover"),
                    ft.Text(producto["nombre"], color="white", weight="bold", size=14, max_lines=1, overflow="ellipsis"),
                    ft.Text(f"Clave: {producto.get('clave', 'N/A')}", color="#f5f5f5", size=13, weight="bold"),
                    
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(f"Costo: ${producto.get('costo', 0.0)}", color="#f5f5f5", weight="bold", size=13),
                            ft.Text(f"Stock: {producto.get('cantidad', 0)}", color="#f5f5f5", weight="bold", size=13),
                        ]
                    ),
                    
                    ft.Text(f"Precio: ${producto['precio']}", color="#ff4081", weight="bold", size=13),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=0,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color="#ffd54f",
                                icon_size=20,
                                on_click=lambda e, p=producto: self.ir_a_editar(p)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color="#e11414",
                                icon_size=20,
                                on_click=lambda e, p_id=producto["id"]: self.eliminar_producto(p_id)
                            ),
                        ]
                    )
                ]
            )
        )

    def eliminar_producto(self, p_id):
        self.page.prod_controller.borrar_producto(p_id)
        self.cambiar_vista("admin_productos")
    
    def ir_a_editar(self, producto):
        self.controlador["producto_editar"] = producto
        self.cambiar_vista("editar_producto")