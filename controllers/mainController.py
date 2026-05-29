import flet as ft

# 1. TUS IMPORTACIONES ORIGINALES ACTUALIZADAS
from views.home import HomeView
from views.fav import FavoritesView
from views.cart import CartView
from views.loginP import LoginView
from views.registerP import RegisterView
from views.admin import AdminView
from views.admin_prod import AdminProductosView
from views.agregar_prod import AgregarProductoView
from views.editar_prod import EditarProductoView
from views.chat_ia import ChatIAView
from views.clientes_View import ClientesView  # <- Nueva importación del chat del Agente

# 2. HERRAMIENTAS DE DATOS Y CONTROLADORES
from models.database import Database
from controllers.producto_controller import ProductoController
from controllers.cliente_controller import ClienteController
from controllers.venta_controller import VentaController
from controllers.ia_controller import IAController  # <- Tu controlador de IA

class MainController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Three Cakes"
        self.page.bgcolor = "#f5f5f5"

        # Inicializamos base de datos y controladores de estado
        Database.inicializar_db()
        self.prod_controller = ProductoController()
        self.cliente_controller = ClienteController()
        self.venta_controller = VentaController()
        
        # 🔥 ACTIVAMOS EL CONTROLADOR DE IA
        self.ia_controller = IAController()
        
        self.usuario_actual = None

        # Compartimos el controlador en la página global
        self.page.prod_controller = self.prod_controller

        # Diccionario global de la app
        self.controlador = {
            "carrito": [],
            "favoritos": [],
            "productos": self.prod_controller.listar_productos()
        }

        self.content = ft.Column(expand=True)

        # 🔥 ACTUALIZAMOS LAS VISTAS ADMITIDAS DEL ADMINISTRADOR
        self.ADMIN_VISTAS = [
            "admin",
            "chat_ia",
            "clientes",
            "admin_productos",
            "agregar_producto",
            "editar_producto"
        ]

        self.drawer = None
        self.blur_bg = None

        self.crear_app()

    def abrir_drawer(self):
        if self.drawer:
            return

        self.blur_bg = ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.3, "black"),
            blur=10,
            on_click=lambda e: self.cerrar_drawer()
        )

        self.drawer = ft.Container(
            width=250,
            height=self.page.height,
            bgcolor="#ff4081",
            right=0,
            top=0,
            padding=20,
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Opciones", size=20, weight="bold", color="white"),
                            ft.IconButton(icon=ft.Icons.CLOSE, icon_color="white", on_click=lambda e: self.cerrar_drawer())
                        ]
                    ),
                    ft.TextButton(
                        "Cerrar sesión",
                        style=ft.ButtonStyle(color="white"),
                        on_click=lambda e: self.cerrar_drawer_y_home()
                    )
                ]
            )
        )

        self.page.overlay.append(self.blur_bg)
        self.page.overlay.append(self.drawer)
        self.page.update()

    def cerrar_drawer(self):
        if self.drawer and self.drawer in self.page.overlay:
            self.page.overlay.remove(self.drawer)
            self.drawer = None

        if self.blur_bg and self.blur_bg in self.page.overlay:
            self.page.overlay.remove(self.blur_bg)
            self.blur_bg = None

        self.page.update()
        
    def cerrar_drawer_y_home(self):
        self.usuario_actual = None
        self.cerrar_drawer()
        self.cambiar_vista("home")

    def crear_navbar(self, vista):
        if vista in ["login", "register"]:
            return ft.Container(
                bgcolor="#ff4081",
                height=60,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT,
                            icon_color="white",
                            on_click=lambda e: self.cambiar_vista("home")
                        ),
                    ]
                )
            )

        elif vista in self.ADMIN_VISTAS:
            return ft.Container(
                bgcolor="#ff4081",
                height=60,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                            icon_color="white",
                            on_click=lambda e: self.cambiar_vista("admin")
                        ),
                    ]
                )
            )

        else:
            return ft.Container(
                bgcolor="#ff4081",
                height=60,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.HOME,
                            icon_color="white",
                            on_click=lambda e: self.cambiar_vista("home")
                        ),
                        ft.IconButton(
                            icon=ft.Icons.FAVORITE,
                            icon_color="white",
                            on_click=lambda e: self.cambiar_vista("favoritos")
                        ),
                        ft.IconButton(
                            icon=ft.Icons.SHOPPING_BAG,
                            icon_color="white",
                            on_click=lambda e: self.cambiar_vista("carrito")
                        ),
                    ]
                )
            )

    def cambiar_vista(self, vista):
        self.content.controls.clear()

        self.controlador["productos"] = self.prod_controller.listar_productos()

        if vista == "home":
            vista_actual = HomeView(self, self.controlador, self.cambiar_vista)
        elif vista == "favoritos":
            vista_actual = FavoritesView(self, self.controlador, self.cambiar_vista)
        elif vista == "carrito":
            vista_actual = CartView(self, self.controlador, self.cambiar_vista)
        elif vista == "login":
            vista_actual = LoginView(self, self.cambiar_vista)
        elif vista == "register":
            vista_actual = RegisterView(self, self.cambiar_vista)
        elif vista == "admin":
            vista_actual = AdminView(self, self.controlador, self.cambiar_vista)
            
        # 🔥 RUTA DEL CHAT IA
        elif vista == "chat_ia":
            vista_actual = ChatIAView(self, self.cambiar_vista)
            
        elif vista == "clientes":
            # IMPORTANTE: Asegúrate de pasar los 3 argumentos (self, controlador, cambiar_vista)
            vista_actual = ClientesView(self, self.controlador, self.cambiar_vista)
            
        elif vista == "admin_productos":
            vista_actual = AdminProductosView(self, self.controlador, self.cambiar_vista)
        elif vista == "agregar_producto":
            vista_actual = AgregarProductoView(self, self.controlador, self.cambiar_vista)
        elif vista == "editar_producto":
            vista_actual = EditarProductoView(self, self.controlador, self.cambiar_vista)
        else:
            vista_actual = ft.Text("Vista no encontrada")

        self.content.controls.append(
            ft.Container(expand=True, content=vista_actual)
        )

        self.app_view.content.controls[1] = self.crear_navbar(vista)
        self.page.update()

    def crear_app(self):
        self.app_view = ft.Container(
            width=390,
            height=800,
            bgcolor="#f5f5f5",
            border_radius=20,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Column(
                expand=True,
                controls=[
                    self.content,
                    self.crear_navbar("home")
                ]
            )
        )

        self.page.add(
            ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.app_view]
            )
        )

        self.cambiar_vista("home")
        
    def accion_perfil(self):
        if self.usuario_actual is None:
            self.cambiar_vista("login")