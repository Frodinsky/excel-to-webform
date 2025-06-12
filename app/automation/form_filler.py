from app.automation.form_controller import FormularioController
import pandas as pd

class FormFiller:
    def __init__(self, file_path):
        self.file_path = file_path

    def ejecutar(self):
        print(f"Ejecutando llenado con: {self.file_path}")
        df = pd.read_excel(self.file_path)
        print(df.head())  # Verifica que se leen los datos

        # Crear solo un controlador
        controlador = FormularioController()

        try:
            for _, fila in df.iterrows():
                datos = {
                    "nombre": fila["nombre"],
                    "email": fila["email"],
                    "dir0": fila["dir0"],
                    "dir1": fila["dir1"]
                }
                print(f"➡️ Llenando: {datos}")
                controlador.llenar_formulario(datos)
        finally:
            controlador.cerrar()
