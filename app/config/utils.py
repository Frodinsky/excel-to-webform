# utils.py
import os

#ruta absoluta del settings.yaml
def get_config_path(filename="settings.yaml", subdir="config"):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, subdir, filename)

