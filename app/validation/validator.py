import pandas as pd
import yaml
from  row_validator import validar_fila

class ValidadorExcel:
    def __init__(self, config_path):
        self.config = self._cargar_configuracion(config_path)
        self.reglas = self.config["validacion"]["campos"]
        excel_path = self.config["validacion"]["archivo_excel"]
        self.df = pd.read_excel(excel_path)

    @staticmethod
    def _cargar_configuracion(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def validar(self):
        reportes = []

        for numero_fila, (_, fila) in enumerate(self.df.iterrows(), start=2):
            errores = validar_fila(fila, self.reglas)
            if errores:
                reportes.append({
                    "fila": numero_fila,
                    "errores": errores
                })

        return reportes
