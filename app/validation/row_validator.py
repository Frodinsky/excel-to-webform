import pandas as pd
import re

TIPOS_VALIDOS = {
    "str": str,                      # Texto plano
    "int": int,                      # Número entero
    "float": float,                  # Número decimal
    "bool": bool,                    # Verdadero / Falso (checkboxes)
    "date": pd.Timestamp,            # Fecha
    "email": str,                    # Texto con validación regex
    "telefono": str,                 # Texto con validación regex
    "dni": str,                      # Documento de identidad, validación personalizada
    "codigo_postal": str,            # CP (numérico o alfanumérico)
    "url": str,                      # Enlace web (input type="url")
    "select": str,                   # Selección de un valor
}

def validar_fila(fila, reglas):
    errores = []

    for campo, regla in reglas.items():
        valor = fila.get(campo, None)

        # Normalizar valor: None, 'None', NaN, etc.
        if isinstance(valor, str):
            valor = valor.strip()
            if valor.lower() == "none":
                valor = ""
        elif pd.isna(valor):
            valor = ""

        # Validación de campo obligatorio
        if valor == "":
            if regla.get("obligatorio", False):
                errores.append(f"{campo} es obligatorio.")
            continue

        # Validación de tipo
        tipo_str = regla.get("tipo")
        tipo_esperado = TIPOS_VALIDOS.get(tipo_str)

        if tipo_esperado:
            if tipo_esperado == pd.Timestamp:
                try:
                    pd.to_datetime(valor, errors='raise')
                except Exception:
                    errores.append(f"{campo} debe ser una fecha válida.")
            else:
                try:
                    if not isinstance(valor, tipo_esperado):
                        valor = tipo_esperado(valor)
                except Exception:
                    errores.append(f"{campo} debe ser de tipo {tipo_str}.")

        # Validación de formato con regex
        regex = regla.get("regex")
        if regex and isinstance(valor, str):
            if not re.fullmatch(regex, valor):
                errores.append(f"{campo} tiene un formato inválido.")

        # Validación por valores permitidos
        valores_permitidos = regla.get("valores")
        if valores_permitidos and valor not in valores_permitidos:
            errores.append(f"{campo} debe ser uno de {valores_permitidos}.")

    return errores
