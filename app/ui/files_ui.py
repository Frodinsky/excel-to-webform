import flet as ft

class FileUploadSection:
    def __init__(self, page: ft.Page):
        self.page = page
        self.theme = page.theme_mode
        self.selected_file_text = ft.Text("Ningún archivo seleccionado", color=ft.Colors.WHITE70, size=16)
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)

        # Color base para resetear el fondo del drop zone
        self.default_bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.WHITE)

        # Se inicializa drop_zone como None para usarla luego
        self.drop_zone = None

    def render(self):
        # Drop zone visual
        self.drop_zone = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(name=ft.Icons.UPLOAD_FILE, size=60, color=ft.Colors.WHITE54),
                    ft.Text("Selecciona tu archivo", size=14, color=ft.Colors.WHITE70),#del de arriba
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            width=300,
            height=150,
            border=ft.border.all(2, ft.Colors.WHITE24),
            border_radius=10,
            bgcolor=self.default_bgcolor,
            alignment=ft.alignment.center,
            on_click=self.select_file,
        )

        # DragTarget para manejar el arrastre de archivos
        drag_target = ft.DragTarget(
            content=self.drop_zone,
            on_accept=self.on_drop,
            on_will_accept=self.on_drag_enter,
            on_leave=self.on_drag_leave
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    drag_target,
                    ft.Container(height=10),
                    self.selected_file_text,

                    ft.ElevatedButton(
                        text="Validar archivo",
                        bgcolor="#3c3c3c",
                        color="white"
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=40,
            border_radius=10,
            width=400,
            alignment=ft.alignment.center
        )

    def select_file(self, e):
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["xlsx", "xls"]
        )

    def on_file_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_name = e.files[0].name
            self.selected_file_text.value = f"{file_name} ✅"
            self.selected_file_text.color = "green"
        else:
            self.selected_file_text.value = "Ningún archivo seleccionado"
            self.selected_file_text.color = ft.Colors.WHITE70
        self.page.update()

    def on_drag_enter(self, e):
        self.drop_zone.bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.WHITE)
        self.page.update()
        return True  # Necesario para aceptar el drop

    def on_drag_leave(self, e):
        self.drop_zone.bgcolor = self.default_bgcolor
        self.page.update()

    def on_drop(self, e):
        # Aquí puedes implementar manejo de archivos si quieres detectar el archivo arrastrado
        # Por ahora, solo mostramos un mensaje
        self.selected_file_text.value = "Archivo arrastrado recibido ✅"
        self.selected_file_text.color = "green"
        self.page.update()
