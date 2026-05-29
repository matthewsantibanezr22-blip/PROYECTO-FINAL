import flet as ft

class FavoritesView(ft.Column):
    def __init__(self, controller, controlador, cambiar_vista):
        super().__init__(expand=True, spacing=10)

        self.controller = controller
        self.controlador = controlador
        self.cambiar_vista = cambiar_vista 

        self.controls = [
            self.top_bar(),
            ft.Container(
                expand=True,
                width=float("inf"),
                content=self.contenido()
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
                        on_click=lambda e: self.controller.abrir_drawer() # BARRA LATERAL ACTIVADA
                    ),
                    ft.Container(
                        width=40,
                        height=40,
                        border_radius=20,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Image(
                            src="xdxdxdxddxd.jpg",
                            fit="cover"
                        ),
                        on_click=lambda e: self.controller.accion_perfil() 
                    )
                ]
            )
        )

    def contenido(self):
        favoritos = self.controlador["favoritos"]
        
        if not favoritos:
            return ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.FAVORITE_BORDER, size=80, color="pink"),
                    ft.Text("Aún no tienes postres favoritos...", size=16, color="black", weight="bold")
                ]
            )
        else:
            list_view = ft.ListView(expand=True, spacing=12, padding=10)
            
            for producto in favoritos:
                
                # Función interna para remover solo de la lista visual en memoria
                def eliminar_favorito(e, prod=producto):
                    self.controlador["favoritos"].remove(prod)
                    self.cambiar_vista("favoritos") # Forzar recarga visual limpia

                list_view.controls.append(
                    ft.Container(
                        bgcolor="#b4b4b4",
                        border_radius=20,
                        padding=12,
                        shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.with_opacity(0.1, "black")),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                # Bloque izquierdo: Imagen + Textos
                                ft.Row(
                                    spacing=12,
                                    controls=[
                                        ft.Container(
                                            width=90,
                                            height=70,
                                            border_radius=10,
                                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                            content=ft.Image(src=producto["imagen"], fit="cover")
                                        ),
                                        ft.Column(
                                            spacing=4,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(producto["nombre"], color="white", weight="bold", size=15),
                                                ft.Text(f"${producto['precio']}", color="#ff4081", weight="bold", size=14),
                                                # Estrellitas decorativas fijas
                                                ft.Row(
                                                    spacing=1,
                                                    controls=[ft.Icon(ft.Icons.STAR, color="yellow", size=14) for _ in range(5)]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                # Botón derecho: Eliminar (X roja)
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color="#e11414",
                                    icon_size=24,
                                    on_click=eliminar_favorito
                                )
                            ]
                        )
                    )
                )
            return list_view