from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver, timeout):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)  # Espera explícita de 10 segundos
        self.username_input_id = "userName"
        self.password_input_id = "userEmail"
        self.address_input_id = "currentAddress"
        self.address2_input_id = "permanentAddress"
        self.login_button_id = "submit"

    def ingresar_usuario(self, nombre):
        campo = self.wait.until(EC.visibility_of_element_located((By.ID, self.username_input_id)))
        campo.clear()
        campo.send_keys(nombre or "")

    def ingresar_email(self, email):
        campo = self.wait.until(EC.visibility_of_element_located((By.ID, self.password_input_id)))
        campo.clear()
        campo.send_keys(email or "")

    def ingresar_direccion1(self, direccion):
        campo = self.wait.until(EC.visibility_of_element_located((By.ID, self.address_input_id)))
        campo.clear()
        campo.send_keys(direccion or "")

    def ingresar_direccion2(self, direccion_permanente):
        campo = self.wait.until(EC.visibility_of_element_located((By.ID, self.address2_input_id)))
        campo.clear()
        campo.send_keys(direccion_permanente or "")

    def hacer_login(self):
        boton = self.wait.until(EC.element_to_be_clickable((By.ID, self.login_button_id)))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", boton)
        self.driver.execute_script("window.scrollBy(0, -100);")
        boton.click()