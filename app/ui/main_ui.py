import flet as ft
from files_ui import FileUploadSection

class FormValidatorApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.theme_mode = ft.ThemeMode.DARK
        self.page.title = "FormValidator"
        self.page.theme_mode = self.theme_mode
        self.page.bgcolor = "#1e1e1e"
        self.page.padding = 20

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
        file_upload_section = FileUploadSection(self.page).render()

        self.page.add(
            theme_toggle_container,
            title_section_container,
            ft.Row([file_upload_section], alignment=ft.MainAxisAlignment.CENTER)
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
