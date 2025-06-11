import os
import yaml
import flet as ft
from app.validation.validator import ValidadorExcel
from app.reports.multi_error_sheets import ReporteErroresMultiplesHojas


class ArchivoValidadorHandler:
    def __init__(self, page: ft.Page):
        self.page = page
        self.result_text = ft.Text(visible=False, size=16)
        self.container = ft.Container(
            content=self.result_text,
            padding=10,
            bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.RED_200),
            border_radius=10,
            visible=False,
        )

    def get_control(self):
        return self.container

    def validate_file(self, file_path: str):
        # Ruta al settings.yaml
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(BASE_DIR, "config/settings.yaml")

        # Actualizar configuración
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        config["validacion"]["archivo_excel"] = file_path
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True)

        # Validar
        validador = ValidadorExcel(config_path=config_path, excel_path=file_path)
        errores = validador.validar()

        if not errores:
            self.result_text.value = "✅ Archivo válido"
            self.result_text.color = "green"
            self.container.bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.GREEN_200)
        else:
            reporte = ReporteErroresMultiplesHojas(errores, ruta_config=config_path)
            ruta_reporte = reporte.exportar()
            self.result_text.value = f"❌ Se encontraron errores.\n📄 Reporte: {ruta_reporte}"
            self.result_text.color = "red"
            self.container.bgcolor = ft.Colors.with_opacity(0.07, ft.Colors.RED_200)

        self.result_text.visible = True
        self.container.visible = True
        self.page.update()
