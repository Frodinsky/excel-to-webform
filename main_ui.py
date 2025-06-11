import flet as ft
from app.ui.files_ui import FileUploadSection
from app.ui.archivo_validador_handler import ArchivoValidadorHandler

class FormValidatorApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.theme_mode = ft.ThemeMode.DARK
        self.page.title = "FormValidator"
        self.page.theme_mode = self.theme_mode
        self.page.bgcolor = "#1e1e1e"
        self.page.padding = 20

        self.validador_handler = None  # ✅ Declarado aquí
        self.file_upload_section = None  # ✅ Declarado aquí

        self.build_ui()

    def build_ui(self):
        theme_toggle_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.BRIGHTNESS_6_OUTLINED,
                        tooltip="Cambiar tema",
                        on_click=self.toggle_theme,
                        icon_color="white"
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            alignment=ft.alignment.top_right
        )

        title_section_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Validador y Automatizador de Formularios",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(color="white24", thickness=1)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            alignment=ft.alignment.center
        )
        # Aquí agregamos el componente modularizado
        self.validador_handler = ArchivoValidadorHandler(self.page)
        self.file_upload_section = FileUploadSection(
            page=self.page,
            on_validate_file=self.validador_handler.validate_file
        )

        self.page.add(
            theme_toggle_container,
            title_section_container,
            ft.Row([self.file_upload_section.render()], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.validador_handler.get_control()], alignment=ft.MainAxisAlignment.CENTER),
        )

    def toggle_theme(self, e):
        self.theme_mode = (
            ft.ThemeMode.LIGHT if self.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        self.page.theme_mode = self.theme_mode
        self.page.bgcolor = "#ffffff" if self.theme_mode == ft.ThemeMode.LIGHT else "#1e1e1e"
        self.page.update()

def main(page: ft.Page):
    FormValidatorApp(page)

ft.app(target=main)
