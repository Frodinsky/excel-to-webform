import flet as ft
import asyncio

class FileUploadSection:
    def __init__(self, page: ft.Page):
        self.page = page
        self.theme = page.theme_mode
        self.selected_file_text = ft.Text("Ningún archivo seleccionado", color=ft.Colors.WHITE70, size=16)

        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)

        # Carga flotante (inicialmente invisible)
        self.loading_indicator = ft.ProgressRing(visible=False, width=30, height=30, color="white")

        # Color base del rectángulo
        self.default_bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.WHITE)

        # Inicializamos el contenedor visual en render
        self.select_area = None

    def render(self):
        self.select_area = ft.Container(
            content=ft.Stack([
                ft.Column(
                    [
                        ft.Icon(name=ft.Icons.UPLOAD_FILE, size=60, color=ft.Colors.WHITE54),
                        ft.Text("Haz clic para seleccionar tu archivo", size=14, color=ft.Colors.WHITE70),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(
                    content=self.loading_indicator,
                    alignment=ft.alignment.top_right,
                    padding=10,
                )
            ]),
            width=300,
            height=150,
            border=ft.border.all(2, ft.Colors.WHITE24),
            border_radius=10,
            bgcolor=self.default_bgcolor,
            alignment=ft.alignment.center,
            on_click=self.select_file,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            scale=1.0,
            on_hover=self.on_hover_effect,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    self.select_area,
                    ft.Container(height=10),
                    self.selected_file_text,
                    ft.ElevatedButton(
                        text="Validar archivo",
                        bgcolor="#3c3c3c",
                        color="white",
                        on_click=self.validate_file
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=80,
            border_radius=10,
            width=450,
            alignment=ft.alignment.center
        )

    def select_file(self, e):
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["xlsx", "xls"]
        )

    def on_file_selected(self, e: ft.FilePickerResultEvent):
        # Mostrar el spinner inmediatamente
        self.loading_indicator.visible = True
        self.page.update()

        # Lanzamos la tarea asincrónica con delay/control
        self.page.run_task(self.finish_loading, e)

    async def finish_loading(self, e: ft.FilePickerResultEvent):
        # Esperamos para simular carga ligera y permitir el render del spinner
        await asyncio.sleep(0.5)

        # Ocultamos el spinner
        self.loading_indicator.visible = False

        # Mostramos el nombre del archivo
        if e.files:
            file_name = e.files[0].name
            self.selected_file_text.value = f"{file_name} ✅"
            self.selected_file_text.color = "green"
        else:
            self.selected_file_text.value = "Ningún archivo seleccionado"
            self.selected_file_text.color = ft.Colors.WHITE70

        self.page.update()

    def on_hover_effect(self, e: ft.ControlEvent):
        self.select_area.scale = 1.15 if e.data == "true" else 1.0
        self.page.update()

    def validate_file(self, e):
        pass
