import flet as ft

class AgregarProductoView(ft.Column):
    # 🔥 Agregamos 'controller' aquí para la barra superior
    def __init__(self, controller, controlador, cambiar_vista):
        super().__init__(expand=True)
        self.controller = controller
        self.controlador = controlador
        self.cambiar_vista = cambiar_vista
        self.controls = [
            self.top_bar(),
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=self.formulario()
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
                        # 🔥 Activamos el Drawer
                        on_click=lambda e: self.controller.abrir_drawer()
                    ),
                    ft.Container(
                        width=40, height=40, border_radius=20,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Image(src="xdxdxdxddxd.jpg", fit="cover"),
                        # 🔥 Activamos el Perfil
                        on_click=lambda e: self.controller.accion_perfil()
                    )
                ]
            )
        )

    def formulario(self):
        # 🎨 ESTÉTICA: Diccionario para unificar un diseño moderno en todos los inputs
        estilo_input = {
            "width": 280,
            "border_radius": 15,
            "filled": True,
            "bgcolor": "#eeeeee",
            "border_color": "transparent",
            "content_padding": 15,
            "focused_border_color": "#ff4081", # Se pinta de tu rosa al seleccionarlo
            "focused_bgcolor": "white"
        }

        # Aplicamos el estilo y agregamos íconos representativos
        nombre = ft.TextField(label="Nombre", prefix_icon=ft.Icons.CAKE, **estilo_input)
        clave = ft.TextField(label="Clave", prefix_icon=ft.Icons.VPN_KEY, **estilo_input)
        costo = ft.TextField(label="Costo", prefix_icon=ft.Icons.ATTACH_MONEY, **estilo_input) 
        cantidad = ft.TextField(label="Cantidad (Stock)", prefix_icon=ft.Icons.INVENTORY, **estilo_input)
        precio = ft.TextField(label="Precio", prefix_icon=ft.Icons.MONETIZATION_ON, **estilo_input)
        img = ft.TextField(label="Ruta de la imagen", prefix_icon=ft.Icons.IMAGE, **estilo_input)

        # 🎨 ESTÉTICA: Metemos la imagen en un contenedor para redondearle los bordes
        preview_container = ft.Container(
            width=120, height=120, 
            border_radius=15, 
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            visible=False,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.1, "black"))
        )
        preview = ft.Image(src="", fit="cover", expand=True)
        preview_container.content = preview

        def actualizar_preview(e):
            if img.value:
                preview.src = img.value
                preview_container.visible = True
                self.update()

        img.on_change = actualizar_preview

        def registrar(e):
            val_precio = float(precio.value) if precio.value else 0.0
            val_costo = float(costo.value) if costo.value else 0.0
            val_cantidad = int(cantidad.value) if cantidad.value else 0
            val_clave = clave.value if clave.value else "SIN-CLAVE"
            val_nombre = nombre.value if nombre.value else "Producto Nuevo"
            val_img = img.value if img.value else "default.jpg"

            self.page.prod_controller.registrar_producto(
                clave=val_clave,
                nombre=val_nombre,
                costo=val_costo,
                precio=val_precio,
                cantidad=val_cantidad,
                imagen=val_img
            )
            self.cambiar_vista("admin_productos")

        return ft.Column(
            width=340, spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO, 
            controls=[
                ft.Text("Agregar producto", size=24, weight="bold", color="black"),
                nombre, clave, costo, cantidad, precio, img, 
                preview_container,
                ft.ElevatedButton(
                    "Registrar producto", 
                    bgcolor="#ff4081", 
                    color="white",
                    width=200, 
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    on_click=registrar
                )
            ]
        )