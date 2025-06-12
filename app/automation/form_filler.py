import pandas as pd
from app.automation.form_controller import FormularioController

class FormFiller:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def ejecutar(self):
        print(f"Usando archivo: {self.file_path}")
        # Lee el Excel, por ejemplo con pandas
        df = pd.read_excel(self.file_path)

        # Asumimos que tomas la primera fila del Excel
        datos = df.iloc[0].to_dict()

        # Ejecutar el llenado del formulario
        formulario = FormularioController()
        formulario.ejecutar(datos_formulario=datos)