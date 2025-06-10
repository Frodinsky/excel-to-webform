import pandas as pd
import yaml
from  row_validator import validar_fila

class ValidadorExcel:
    def __init__(self, config_path):
        self.config = self._cargar_configuracion(config_path)
        self.reglas = self.config["validacion"]["campos"]
        self.excel_path = self.config["validacion"]["archivo_excel"]
        # Si el usuario no especifica las hojas, detectarlas automáticamente
        self.hojas = self.config["validacion"].get("hojas")
        if not self.hojas:
            self.hojas = self._obtener_hojas()
        self.dfs = self._leer_hojas()

    @staticmethod
    def _cargar_configuracion(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _obtener_hojas(self):
        excel_file = pd.ExcelFile(self.excel_path)
        return excel_file.sheet_names  # Lista de nombres de hojas

    def _leer_hojas(self):
        if not self.hojas:
            # Leer solo la hoja por defecto
            df = pd.read_excel(self.excel_path)
            return {"Hoja1": df}
        else:
            # Leer solo las hojas especificadas
            dfs = {}
            for hoja in self.hojas:
                dfs[hoja] = pd.read_excel(self.excel_path, sheet_name=hoja)
            return dfs

    def validar(self):
        reporte_por_hoja = {}

        for hoja, df in self.dfs.items():
            errores = []
            for numero_fila, (_, fila) in enumerate(df.iterrows(), start=2):
                errores_fila = validar_fila(fila, self.reglas)
                if errores_fila:
                    errores.append({
                        "fila": numero_fila,
                        "errores": errores_fila
                    })
            if errores:
                reporte_por_hoja[hoja] = {
                    "df": df,
                    "errores": errores
                }

        return reporte_por_hoja
