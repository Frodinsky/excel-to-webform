import flet as ft
import asyncio
from app.automation.form_filler import FormFiller


class ProgressBarHandler:
    def __init__(self, page: ft.Page):
        self.page = page
        self.progress_bar = ft.ProgressBar(width=300, height=20, visible=False)
        self.container = ft.Container(
            content=self.progress_bar,
            padding=10,
            visible=False,
            border_radius=10,
        )

    def get_control(self):
        return self.container

    def show(self):
        self.progress_bar.value = 0
        self.progress_bar.visible = True
        self.container.visible = True
        self.page.update()

    def hide(self):
        self.progress_bar.visible = False
        self.container.visible = False
        self.page.update()

    def set_value(self, value: float):
        self.progress_bar.value = value
        self.page.update()

    async def ejecutar_llenado_async(self, file_path: str):
        if not file_path:
            return

        self.show()

        form_filler = FormFiller(file_path)

        def progress_callback(value):
            self.set_value(value)

        form_filler.set_progress_callback(progress_callback)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, form_filler.ejecutar)

        self.hide()
