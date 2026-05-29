import flet as ft
import time

class CartView(ft.Column):
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
        carrito = self.controlador["carrito"]
        
        if not carrito:
            return ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, size=80, color="pink"),
                    ft.Text("Carrito de compra vacío...", size=16, color="black", weight="bold")
                ]
            )
        else:
            total = sum(p["precio"] for p in carrito)
            list_view = ft.ListView(expand=True, spacing=12, padding=10)
            
            for producto in carrito:
                def eliminar_del_carrito(e, prod=producto):
                    self.controlador["carrito"].remove(prod)
                    self.cambiar_vista("carrito") # Forzar recarga visual limpia

                list_view.controls.append(
                    ft.Container(
                        bgcolor="#b4b4b4",
                        border_radius=20,
                        padding=12,
                        shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.with_opacity(0.1, "black")),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
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
                                                ft.Row(
                                                    spacing=1,
                                                    controls=[ft.Icon(ft.Icons.STAR, color="yellow", size=14) for _ in range(5)]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color="#e11414",
                                    icon_size=24,
                                    on_click=eliminar_del_carrito
                                )
                            ]
                        )
                    )
                )

            # 🔥 Etiqueta para mensajes de compra (Éxito o Error)
            self.lbl_mensaje = ft.Text("", weight="bold", size=14, text_align=ft.TextAlign.CENTER)

            return ft.Column(
                expand=True,
                controls=[
                    list_view,
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, bottom=25, top=10),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Total a Pagar: ", size=24, weight="bold", color="black"),
                                        ft.Text(f"${total:.2f}", size=24, weight="bold", color="#11c66f")
                                    ]
                                ),
                                self.lbl_mensaje, # 🔥 Aparece justo arriba del botón
                                ft.ElevatedButton(
                                    content=ft.Text("Comprar", size=18, weight="bold", color="white"),
                                    bgcolor="#ff4081",
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(horizontal=50, vertical=15),
                                        shape=ft.RoundedRectangleBorder(radius=15)
                                    ),
                                    on_click=self.procesar_pago # 🔥 Llamada a la nueva función
                                )
                            ]
                        )
                    )
                ]
            )

    def procesar_pago(self, e):
        carrito = self.controlador["carrito"]
        
        # 1. Llamar al controlador de ventas
        exito, msj = self.controller.venta_controller.procesar_carrito(carrito)
        
        if exito:
            # 2. Si todo sale bien, pintar verde, vaciar carrito y recargar
            self.lbl_mensaje.value = msj
            self.lbl_mensaje.color = "#11c66f"
            self.update()
            
            self.controlador["carrito"] = [] # Se vacía la lista en memoria
            time.sleep(1.5) # Pausa para que el usuario lea el mensaje de éxito
            self.cambiar_vista("carrito") # Recarga la vista para que aparezca "Carrito vacío"
        else:
            # 3. Si no hay stock o falla, pintar rojo
            self.lbl_mensaje.value = msj
            self.lbl_mensaje.color = "#e11414"
            self.update()