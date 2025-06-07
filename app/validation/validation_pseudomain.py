import os
from validator import ValidadorExcel
from report_generator import ReporteErroresExcel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config/settings.yaml")

if __name__ == "__main__":
    validador = ValidadorExcel(CONFIG_PATH)
    errores = validador.validar()

    if errores:
        print(f"❌ Se encontraron errores en {len(errores)} fila(s).")
        reporte = ReporteErroresExcel(validador.df, errores, CONFIG_PATH)
        reporte.exportar()
    else:
        print("✅ Todos los datos son válidos.")
