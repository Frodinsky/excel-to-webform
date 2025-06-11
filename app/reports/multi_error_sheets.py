import pandas as pd
from app.reports.report_generator import ReporteErroresExcel
import os

class ReporteErroresMultiplesHojas:
    def __init__(self, reporte_por_hoja, ruta_config=None, ruta_salida="errores_completo.xlsx"):
        if ruta_config is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ruta_config = os.path.join(base_dir, "config/settings.yaml")

        self.reporte_por_hoja = reporte_por_hoja
        self.ruta_config = ruta_config
        self.ruta_salida = ruta_salida

    def exportar(self):
        """Genera un archivo Excel con múltiples hojas, cada una con errores resaltados."""
        with pd.ExcelWriter(self.ruta_salida, engine="openpyxl", mode="w") as writer:
            for nombre_hoja, datos in self.reporte_por_hoja.items():
                df = datos["df"]
                errores = datos["errores"]

                # Reutiliza la clase original para exportar hoja por hoja
                reporte = ReporteErroresExcel(df, errores, ruta_config=self.ruta_config)
                reporte.exportar(writer=writer, nombre_hoja=nombre_hoja)

        print(f"📘 Reporte consolidado generado: {self.ruta_salida}")
