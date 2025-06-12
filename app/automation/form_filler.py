import pandas as pd
from app.automation.form_controller import FormularioController

class FormFiller:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path

    def ejecutar(self):
        # Lee el Excel, por ejemplo con pandas
        df = pd.read_excel(self.excel_path)

        # Asumimos que tomas la primera fila del Excel
        datos = df.iloc[0].to_dict()

        # Ejecutar el llenado del formulario
        formulario = FormularioController()
        formulario.ejecutar(datos_formulario=datos)