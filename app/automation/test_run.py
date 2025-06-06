from form_controller import FormularioController

def main():
    # Datos de ejemplo para llenar el formulario
    datos_formulario = {
        "nombre": "Juan Pérez",
        "email": "juan.perez@example.com",
        "direccion1": "Calle Falsa 123",
        "direccion2": "Colonia Inventada"
    }

    # Crear instancia del controlador con ruta al YAML si usas diferente
    controller = FormularioController()

    # Ejecutar el llenado del formulario
    controller.ejecutar(datos_formulario)

if __name__ == "__main__":
    main()
