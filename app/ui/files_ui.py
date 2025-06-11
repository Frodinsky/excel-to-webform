import flet as ft
import asyncio
from app.validation.validator import ValidadorExcel
from app.reports.multi_error_sheets import ReporteErroresMultiplesHojas
import yaml
import os

class FileUploadSection:
    def __init__(self, page: ft.Page):
        self.page = page
        self.theme = page.theme_mode
        self.selected_file_text = ft.Text("Ningún archivo seleccionado", color=ft.Colors.WHITE70, size=16)

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
            width=self.page.width * 0.53,  # ✅ Aproximadamente 33% del ancho
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
            disabled=True,  # ✅ Inicia desactivado
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
            self.validate_button.disabled = False  # ✅ Activar botón
        else:
            self.selected_file_text.value = "Ningún archivo seleccionado"
            self.selected_file_text.color = ft.Colors.WHITE70

        self.page.update()

    def on_hover_effect(self, e: ft.ControlEvent):
        self.select_area.scale = 1.15 if e.data == "true" else 1.0
        self.page.update()

    def validate_file(self, e):
        if not self.selected_file_path:
            self.selected_file_text.value = "⚠️ Primero selecciona un archivo."
            self.selected_file_text.color = "orange"
            self.page.update()
            return

        # ✅ Ruta absoluta al settings.yaml
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(BASE_DIR, "config/settings.yaml")

        # ✅ Cargar configuración y actualizar path del Excel
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        config["validacion"]["archivo_excel"] = self.selected_file_path

        # ✅ Guardar cambios en el mismo settings.yaml
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True)

        # ✅ Ejecutar validación
        validador = ValidadorExcel(config_path=config_path, excel_path=self.selected_file_path)
        reporte_por_hoja = validador.validar()

        if not reporte_por_hoja:
            self.selected_file_text.value = "✅ Archivo válido"
            self.selected_file_text.color = "green"
        else:
            self.selected_file_text.value = "❌ Archivo con errores"
            self.selected_file_text.color = "red"
            # ✅ Pasar también config_path al reporte
            reporte = ReporteErroresMultiplesHojas(reporte_por_hoja, ruta_config=config_path)
            reporte.exportar()

        self.page.update()

