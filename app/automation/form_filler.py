from app.automation.form_controller import FormularioController
import pandas as pd

class FormFiller:
    def __init__(self, file_path):
        self.file_path = file_path
        self.progress_callback = None

    def set_progress_callback(self, callback):
        self.progress_callback = callback

    def ejecutar(self):
        #print(f"Ejecutando llenado con: {self.file_path}")
        df = pd.read_excel(self.file_path)
        #print(df.head())  # Verifica que se leen los datos

        total = len(df)
        controlador = FormularioController()

        try:
            for i, (_, fila) in enumerate(df.iterrows(), 1):
                datos = {
                    "nombre": fila["nombre"],
                    "email": fila["email"],
                    "dir0": fila["dir0"],
                    "dir1": fila["dir1"]
                }
                #print(f"➡️ Llenando: {datos}")
                controlador.llenar_formulario(datos)

                # Reportar progreso (valor entre 0 y 1)
                if self.progress_callback:
                    progreso = i / total
                    self.progress_callback(progreso)
        finally:
            controlador.cerrar()
