import os
from validator import ValidadorExcel
from app.reports.multi_error_sheets import ReporteErroresMultiplesHojas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config/settings.yaml")

if __name__ == "__main__":
    validador = ValidadorExcel(CONFIG_PATH)
    reporte_por_hoja = validador.validar()

    if not reporte_por_hoja:
        print("✅ Todos los datos son válidos.")
    else:
        total_errores = sum(len(d["errores"]) for d in reporte_por_hoja.values())
        print(f"❌ Se encontraron errores en {total_errores} fila(s) con errores.")

        reporte = ReporteErroresMultiplesHojas(reporte_por_hoja, ruta_config=CONFIG_PATH)
        reporte.exportar()
