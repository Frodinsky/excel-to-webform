import os
import yaml
import flet as ft
from app.validation.validator import ValidadorExcel
from app.reports.multi_error_sheets import ReporteErroresMultiplesHojas
from app.automation.form_filler import FormFiller
from app.ui.progress_bar_handler import ProgressBarHandler

class ArchivoValidadorHandler:
    def __init__(self, page: ft.Page):
        self.page = page
        self.result_text = ft.Text(visible=False, size=16)
        self.file_path = None
        self.progress_bar_handler = ProgressBarHandler(page)
        self.automation_button = ft.ElevatedButton(
            text="Llenar Formulario",
            visible=False,
            on_click = lambda e: self.iniciar_llenado_async()
        )
        self.container = ft.Container(
            content=ft.Column(
                controls=[
                    self.result_text,
                    self.automation_button,
                    self.progress_bar_handler.get_control(),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=10,
            bgcolor=ft.Colors.with_opacity(0.17, ft.Colors.RED_200),
            border_radius=10,
            visible=False,
        )

    def get_control(self):
        return ft.Column([
            self.container,  # tu actual UI con resultado y botón
            self.progress_bar_handler.get_control()
        ])

    def validate_file(self, file_path: str):
        self.file_path = file_path
        # Ruta al settings.yaml
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(BASE_DIR, "config/settings.yaml")

        # Leer la configuración (sin modificarla)
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Validar (sin tocar el YAML)
        validador = ValidadorExcel(config_path=config_path, excel_path=file_path)
        errores = validador.validar()

        if not errores:
            self.result_text.value = "✅ Archivo válido"
            self.result_text.color = "green"
            self.container.bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.GREEN_200)
            self.automation_button.visible = True
        else:
            reporte = ReporteErroresMultiplesHojas(errores, ruta_config=config_path)
            ruta_reporte = reporte.exportar()
            self.result_text.value = f"❌ Se creo un archivo {ruta_reporte}"
            self.result_text.color = "red"
            self.container.bgcolor = ft.Colors.with_opacity(0.07, ft.Colors.RED_200)
            self.automation_button.visible = False

        self.result_text.visible = True
        self.container.visible = True
        self.page.update()

    def ejecutar_llenado(self, e):
        if self.file_path:
            print("Ejecutando llenado con:", self.file_path)
            try:
                llenador = FormFiller(self.file_path)
                llenador.ejecutar()
                self.page.snack_bar = ft.SnackBar(ft.Text("✅ Formulario enviado con éxito"))
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error al llenar formulario: {str(ex)}"))
            self.page.snack_bar.open = True
            self.page.update()

    def iniciar_llenado_async(self):
        self.page.run_task(self._run_llenado_async)

    async def _run_llenado_async(self):
        await self.progress_bar_handler.ejecutar_llenado_async(self.file_path)



