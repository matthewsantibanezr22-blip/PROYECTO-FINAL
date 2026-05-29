import flet as ft
import time

class RegisterView(ft.Column):
    def __init__(self, controller, cambiar_vista):
        super().__init__(expand=True)
        self.controller = controller
        self.cambiar_vista = cambiar_vista

        self.txt_user = ft.TextField(
            label="Usuario", 
            prefix_icon=ft.Icons.PERSON,
            width=280
        )
        self.txt_correo = ft.TextField(
            label="Correo Electrónico", 
            prefix_icon=ft.Icons.EMAIL,
            width=280
        )
        self.txt_pass = ft.TextField(
            label="Contraseña", 
            prefix_icon=ft.Icons.LOCK, 
            password=True, 
            can_reveal_password=True,
            width=280
        )

        # 🔥 Texto de advertencia arriba del botón
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
                            "Crear Cuenta",
                            size=30,
                            weight="bold",
                            color="#ff4081"
                        ),
                        ft.Container(height=10), 
                        self.txt_user,
                        self.txt_correo,
                        self.txt_pass,
                        ft.Container(height=5),
                        self.lbl_error, # 🔥 Colocado justo arriba del botón
                        ft.Container(height=5), 
                        ft.ElevatedButton(
                            "Registrarse",
                            bgcolor="#ff4081",
                            color="white",
                            width=200,
                            height=45,
                            on_click=self.hacer_registro
                        ),
                        ft.TextButton(
                            "¿Ya tienes cuenta? Inicia sesión",
                            style=ft.ButtonStyle(color="#ff4081"),
                            on_click=lambda e: self.cambiar_vista("login")
                        )
                    ]
                )
            )
        ]

    def hacer_registro(self, e):
        user_val = self.txt_user.value.strip() if self.txt_user.value else ""
        correo_val = self.txt_correo.value.strip() if self.txt_correo.value else ""
        pass_val = self.txt_pass.value.strip() if self.txt_pass.value else ""

        # 1. Validar campos vacíos
        if not user_val or not correo_val or not pass_val:
            self.lbl_error.value = "Por favor, llena todos los campos. ❌"
            self.lbl_error.color = "#e11414"
            self.update()
            return

        # 2. Mandar al controlador
        exito, msj = self.controller.cliente_controller.register(user_val, correo_val, pass_val)
        
        if exito:
            # Si sale bien, lo pintamos verde, pausamos medio segundo para que lo lea y lo mandamos al login
            self.lbl_error.value = msj
            self.lbl_error.color = "#11c66f" # Verde
            self.update()
            time.sleep(0.8) 
            self.cambiar_vista("login") 
        else:
            # Si ya existe, pintamos rojo
            self.lbl_error.value = msj
            self.lbl_error.color = "#e11414"
            self.update()