import pandas as pd
from report_generator import ReporteErroresExcel

class ReporteErroresMultiplesHojas:
    def __init__(self, reporte_por_hoja, ruta_config="settings.yaml", ruta_salida="errores_completo.xlsx"):

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
