import flet as ft
import asyncio

class FileUploadSection:
    def __init__(self, page: ft.Page, on_validate_file):
        self.page = page
        self.theme = page.theme_mode
        self.selected_file_text = ft.Text("Ningún archivo seleccionado", color=ft.Colors.WHITE70, size=16)
        self.on_validate_file = on_validate_file
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)

        self.loading_indicator = ft.ProgressRing(visible=False, width=30, height=30, color="white")
        self.default_bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.WHITE)

        self.select_area = None
        self.spinner_overlay = None
        self.selected_file_path = None
        self.validate_button = None

    def render(self):
        self.select_area = ft.Container(
            content=ft.Stack([
                # Contenedor centrado de ícono y texto
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(name=ft.Icons.UPLOAD_FILE, size=60, color=ft.Colors.WHITE54),
                            ft.Text("Haz clic para seleccionar tu archivo", size=16, color=ft.Colors.WHITE70),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                # Indicador flotante
                ft.Container(
                    content=self.loading_indicator,
                    alignment=ft.alignment.top_right,
                    padding=10,
                )
            ]),
            width=self.page.width * 0.66,  # ✅ Aproximadamente 33% del ancho
            height=200,  # ✅ Un poco más alto
            border=ft.border.all(2, ft.Colors.WHITE24),
            border_radius=10,
            bgcolor=self.default_bgcolor,
            alignment=ft.alignment.center,
            on_click=self.select_file,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            scale=1.0,
            on_hover=self.on_hover_effect,
        )

        self.validate_button = ft.ElevatedButton(
            text="Validar archivo",
            bgcolor="#3c3c3c",
            color="white",
            on_click=self.validate_file,
            visible=False,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    self.select_area,
                    ft.Container(height=10),
                    self.selected_file_text,
                    self.validate_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=80,
            border_radius=10,
            width=850,
            alignment=ft.alignment.center,
        )


    def select_file(self, e):
        # Sombra azul temporal
        self.select_area.shadow = ft.BoxShadow(
            spread_radius=4,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLUE),
            offset=ft.Offset(0, 0),
        )
        self.page.update()

        # Remover la sombra luego de 200ms
        self.page.run_task(self.remove_shadow)

        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["xlsx", "xls"]
        )

    async def remove_shadow(self):
        await asyncio.sleep(1)
        self.select_area.shadow = None
        self.page.update()

    def on_file_selected(self, e: ft.FilePickerResultEvent):
        self.loading_indicator.visible = True
        self.page.update()
        self.page.run_task(self.finish_loading, e)

    async def finish_loading(self, e: ft.FilePickerResultEvent):
        await asyncio.sleep(0.5)
        self.loading_indicator.visible = False

        if e.files:
            file_name = e.files[0].name
            self.selected_file_text.value = f"{file_name} ✅"
            self.selected_file_text.color = "green"
            self.selected_file_path = e.files[0].path  # ✅ Guardar path real
            self.validate_button.visible = True  # ✅ Activar botón
        else:
            self.selected_file_text.value = "Ningún archivo seleccionado"
            self.selected_file_text.color = ft.Colors.WHITE70
            self.validate_button.visible = False

        self.page.update()

    def on_hover_effect(self, e: ft.ControlEvent):
        self.select_area.scale = 1.15 if e.data == "true" else 1.0
        self.page.update()

    def validate_file(self, e):
        self.on_validate_file(self.selected_file_path)


