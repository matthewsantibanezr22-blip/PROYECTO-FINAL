import flet as ft

class LoginView(ft.Column):
    def __init__(self, controller, cambiar_vista):
        super().__init__(expand=True)
        self.controller = controller
        self.cambiar_vista = cambiar_vista

        self.txt_user = ft.TextField(
            label="Usuario", 
            prefix_icon=ft.Icons.PERSON,
            width=280
        )
        self.txt_pass = ft.TextField(
            label="Contraseña", 
            prefix_icon=ft.Icons.LOCK, 
            password=True, 
            can_reveal_password=True,
            width=280
        )
        
        # 🔥 Este es el texto que aparecerá arriba del botón
        self.lbl_error = ft.Text("", color="#e11414", weight="bold", size=14)

        self.controls = [
            ft.Container(
                expand=True,
                width=float("inf"),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Iniciar Sesión",
                            size=30,
                            weight="bold",
                            color="#ff4081"
                        ),
                        ft.Container(height=10), 
                        self.txt_user,
                        self.txt_pass,
                        ft.Container(height=5),
                        self.lbl_error, # 🔥 Aquí colocamos el texto de advertencia
                        ft.Container(height=5), 
                        ft.ElevatedButton(
                            "Ingresar",
                            bgcolor="#ff4081",
                            color="white",
                            width=200,
                            height=45,
                            on_click=self.hacer_login
                        ),
                        ft.TextButton(
                            "¿No tienes cuenta? Regístrate",
                            style=ft.ButtonStyle(color="#ff4081"),
                            on_click=lambda e: self.cambiar_vista("register")
                        )
                    ]
                )
            )
        ]

    def hacer_login(self, e):
        user_val = self.txt_user.value.strip() if self.txt_user.value else ""
        pass_val = self.txt_pass.value.strip() if self.txt_pass.value else ""

        # 1. Validar campos vacíos
        if not user_val or not pass_val:
            self.lbl_error.value = "Por favor, llena todos los campos. ❌"
            self.lbl_error.color = "#e11414" # Rojo
            self.update() # Actualiza solo esta vista
            return

        # 2. Consultar al controlador
        exito, resultado = self.controller.cliente_controller.login(user_val, pass_val)
        
        if exito:
            self.lbl_error.value = ""
            self.controller.usuario_actual = resultado
            if resultado.rol == "administrador":
                self.cambiar_vista("admin") 
            else:
                self.cambiar_vista("home")  
        else:
            # 3. Mostrar advertencia si se equivocaron de datos
            self.lbl_error.value = resultado
            self.lbl_error.color = "#e11414"
            self.update()