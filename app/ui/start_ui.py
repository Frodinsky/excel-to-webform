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
        self.page.padding = 50

        self.validador_handler = None  # ✅ Declarado aquí
        self.file_upload_section = None  # ✅ Declarado aquí

        self.build_ui()

    def ocultar_boton_validar(self):
        self.file_upload_section.validate_button.visible = False
        self.page.update()

    def build_ui(self):
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
            padding=ft.padding.only(top=100),
            alignment=ft.alignment.center,

        )
        # Aquí agregamos el componente modularizado
        self.validador_handler = ArchivoValidadorHandler(
            page=self.page,
            on_valid=self.ocultar_boton_validar  # 👈 Aquí conectas el paso 3
        )
        self.file_upload_section = FileUploadSection(
            page=self.page,
            on_validate_file=self.validador_handler.validate_file
        )

        self.page.add(
            title_section_container,
            ft.Row([self.file_upload_section.render()], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.validador_handler.get_control()], alignment=ft.MainAxisAlignment.CENTER),
        )


def start_ui(page: ft.Page):
    FormValidatorApp(page)

