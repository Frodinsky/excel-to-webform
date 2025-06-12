from app.automation.login_page import LoginPage
import yaml
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class FormularioController:
    def __init__(self, config_path=None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config", "settings.yaml")
        self.config = self.cargar_config(config_path)
        self.driver = self.crear_driver()

    @staticmethod
    def cargar_config(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def crear_driver(self):
        options = Options()
        if self.config["selenium"].get("headless"):
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        if self.config["selenium"].get("maximizar"):
            driver.maximize_window()
        return driver

    def ejecutar(self, datos_formulario: dict):
        try:
            self.driver.get(self.config["selenium"]["url_formulario"])
            login_page = LoginPage(self.driver, timeout=self.config["selenium"]["timeout"])
            login_page.ingresar_usuario(datos_formulario.get("nombre"))
            login_page.ingresar_email(datos_formulario.get("email"))
            login_page.ingresar_direccion1(datos_formulario.get("direccion1"))
            login_page.ingresar_direccion2(datos_formulario.get("direccion2"))
            login_page.hacer_login()
            time.sleep(2)
        finally:
            self.driver.quit()
