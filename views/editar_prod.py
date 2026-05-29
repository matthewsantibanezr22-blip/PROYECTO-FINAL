import flet as ft

class EditarProductoView(ft.Column):
    # 🔥 Agregamos 'controller' para la barra superior
    def __init__(self, controller, controlador, cambiar_vista):
        super().__init__(expand=True)
        self.controller = controller
        self.controlador = controlador
        self.cambiar_vista = cambiar_vista
        
        self.producto = self.controlador.get("producto_editar", {})

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
        # 🎨 ESTÉTICA: Reutilizamos el mismo diccionario de estilo para mantener consistencia
        estilo_input = {
            "width": 280,
            "border_radius": 15,
            "filled": True,
            "bgcolor": "#eeeeee",
            "border_color": "transparent",
            "content_padding": 15,
            "focused_border_color": "#ff4081",
            "focused_bgcolor": "white"
        }

        # Aplicamos el estilo, los íconos y cargamos los values del producto
        nombre = ft.TextField(label="Nombre", value=self.producto.get("nombre", ""), prefix_icon=ft.Icons.CAKE, **estilo_input)
        clave = ft.TextField(label="Clave", value=self.producto.get("clave", ""), prefix_icon=ft.Icons.VPN_KEY, **estilo_input)
        costo = ft.TextField(label="Costo", value=str(self.producto.get("costo", 0.0)), prefix_icon=ft.Icons.ATTACH_MONEY, **estilo_input)
        cantidad = ft.TextField(label="Cantidad (Stock)", value=str(self.producto.get("cantidad", 0)), prefix_icon=ft.Icons.INVENTORY, **estilo_input)
        precio = ft.TextField(label="Precio", value=str(self.producto.get("precio", 0.0)), prefix_icon=ft.Icons.MONETIZATION_ON, **estilo_input)
        img = ft.TextField(label="Ruta de la imagen", value=self.producto.get("imagen", ""), prefix_icon=ft.Icons.IMAGE, **estilo_input)

        # 🎨 ESTÉTICA: Contenedor para que la previsualización se vea moderna
        preview_container = ft.Container(
            width=120, height=120,
            border_radius=15,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            visible=True if img.value else False,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.1, "black"))
        )
        preview = ft.Image(src=img.value, fit="cover", expand=True)
        preview_container.content = preview

        def actualizar_preview(e):
            if img.value:
                preview.src = img.value
                preview_container.visible = True
                self.update()

        img.on_change = actualizar_preview

        def guardar_cambios(e):
            val_costo = float(costo.value) if costo.value else 0.0
            
            self.page.prod_controller.modificar_producto(
                id_prod=self.producto.get("id"),
                clave=clave.value,
                nombre=nombre.value,
                costo=val_costo,
                precio=float(precio.value) if precio.value else 0.0,
                cantidad=int(cantidad.value) if cantidad.value else 0,
                imagen=img.value
            )
            self.cambiar_vista("admin_productos")

        return ft.Column(
            width=340, spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Editar producto", size=24, weight="bold", color="black"),
                nombre, clave, costo, cantidad, precio, img, 
                preview_container,
                ft.ElevatedButton(
                    "Guardar cambios", 
                    bgcolor="#ff4081", 
                    color="white",
                    width=200, 
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    on_click=guardar_cambios
                )
            ]
        )