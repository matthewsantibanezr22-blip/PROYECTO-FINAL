import flet as ft
import asyncio

class ChatIAView(ft.Column):
    def __init__(self, controller, cambiar_vista):
        super().__init__(expand=True, spacing=10)
        self.controller = controller
        self.cambiar_vista = cambiar_vista
        self.modo_inicio = True

        # 1. Contenedor de mensajes del Chat con Auto-Scroll
        self.chat = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )

        # 2. Inputs adaptados al diseño responsivo de la App
        self.txt_inicio = ft.TextField(
            hint_text="¿Qué quieres calcular hoy, bro?",
            expand=True,
            border_radius=15,
            bgcolor="#f5f5f5",
            border_color="#ff4081",
            on_submit=self.enviar_mensaje
        )

        self.txt_chat = ft.TextField(
            hint_text="Pregúntale al Agente Financiero...",
            expand=True,
            border_radius=15,
            bgcolor="#f5f5f5",
            border_color="#ff4081",
            on_submit=self.enviar_mensaje,
            visible=False
        )

        self.btn_enviar = ft.IconButton(
            icon=ft.Icons.SEND_ROUNDED,
            icon_color="#ff4081",
            icon_size=28,
            on_click=self.enviar_mensaje
        )

        # 3. DISEÑO: Vista de Bienvenida
        self.vista_inicio = ft.Container(
            expand=True,
            animate_opacity=300,
            opacity=1,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Icon(ft.Icons.ANALYTICS_ROUNDED, size=60, color="#ff4081"),
                    ft.Text(
                        "¿Por dónde deberíamos empezar?",
                        size=20,
                        weight="bold",
                        color="black",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Row(
                        controls=[self.txt_inicio, self.btn_enviar],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )

        # 4. DISEÑO: Vista del Chat Activo
        self.vista_chat = ft.Container(
            expand=True,
            opacity=0,
            animate_opacity=300,
            visible=False,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Agente Financiero IA", size=22, weight="bold", color="black"),
                    
                    ft.Container(
                        expand=True,
                        content=self.chat,
                        border=ft.border.all(1, "#e0e0e0"),
                        padding=12,
                        border_radius=20,
                        bgcolor="#fafafa"
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    
                    ft.Row(
                        controls=[self.txt_chat, self.btn_enviar],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )

        self.controls = [
            self.top_bar(),
            self.vista_inicio,
            self.vista_chat
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
                        content=ft.Image(
                            src="xdxdxdxddxd.jpg",
                            fit="cover"
                        ),
                        on_click=lambda e: self.controller.accion_perfil() 
                    )
                ]
            )
        )

    def burbuja_usuario(self, mensaje):
        ancho_dinamico = 260 if len(mensaje) > 25 else None
        return ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.Container(
                    content=ft.Text(mensaje, color="black", size=14),
                    bgcolor="#e0e0e0",
                    padding=12,
                    width=ancho_dinamico,
                    border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15)
                )
            ]
        )

    def burbuja_ia(self, mensaje):
        ancho_dinamico = 260 if len(mensaje) > 25 else None
        return ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Container(
                    content=ft.Text(mensaje, color="black", size=14, selectable=True),
                    bgcolor="#fce4ec", 
                    padding=12,
                    width=ancho_dinamico,
                    border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=15)
                )
            ]
        )

    async def enviar_mensaje(self, e):
        mensaje = self.txt_inicio.value.strip() if self.modo_inicio else self.txt_chat.value.strip()

        if not mensaje:
            return

        if self.modo_inicio:
            self.modo_inicio = False
            self.txt_inicio.value = ""
            self.vista_inicio.opacity = 0
            self.update()
            await asyncio.sleep(0.3)
            
            self.vista_inicio.visible = False
            self.vista_chat.visible = True
            self.txt_chat.visible = True
            self.vista_chat.opacity = 1
            self.update()

        self.chat.controls.append(self.burbuja_usuario(mensaje))
        if not self.modo_inicio:
            self.txt_chat.value = ""

        self.txt_chat.disabled = True
        self.btn_enviar.disabled = True
        
        escribiendo = self.burbuja_ia("Entrenando red neuronal y analizando cuentas...")
        self.chat.controls.append(escribiendo)
        self.chat.scroll_to(delta=100, duration=200)
        self.update()

        try:
            # Mandamos la petición al hilo secundario para evitar congelar la interfaz de Flet
            respuesta = await asyncio.to_thread(
                self.controller.ia_controller.preguntar_asistente, 
                mensaje
            )
        except Exception as ex:
            respuesta = f"Hubo un detalle al conectar con el cerebro de IA, bro: {ex}"

        self.chat.controls.remove(escribiendo)
        self.chat.controls.append(self.burbuja_ia(respuesta))

        self.txt_chat.disabled = False
        self.btn_enviar.disabled = False
        self.chat.scroll_to(delta=200, duration=200)
        self.update()