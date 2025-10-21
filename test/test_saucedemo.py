import pytest
import sys
import os
from selenium.webdriver.common.by import By
from pathlib import Path
import time

sauce_demo_dir = Path(__file__).parent
screenshots_dir = sauce_demo_dir / "screenshots"
screenshots_dir.mkdir(exist_ok=True, parents=True)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.helpers import login_saucedemo, get_driver

@pytest.fixture(scope='function')  # Cambio aquí para abrir navegador por test
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope='function')  # Fixture ya que hace login antes de cada test
def logged_in_driver(driver):
    login_saucedemo(driver)
    #Aqui espera para asegurarse que cargó la pag
    time.sleep(2)
    yield driver

def test_login(logged_in_driver): #LOGIN
    assert "/inventory.html" in logged_in_driver.current_url

def test_ver_productos(logged_in_driver): #Aqui que se pueda ver el catalogo de productos
    productos = logged_in_driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0

def test_agregar_producto_al_carrito(logged_in_driver): #Que se pueda agregar un producto al carrito
    boton_agregar = logged_in_driver.find_element(By.XPATH, "(//button[contains(text(),'Add to cart')])[1]")
    boton_agregar.click()
    time.sleep(1)
    contador = logged_in_driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert contador == "1"

def test_ver_producto_en_carrito(logged_in_driver): #Que se vea el producto en el carrito
    #aqui debe agregar producto
    logged_in_driver.find_element(By.XPATH, "(//button[contains(text(),'Add to cart')])[1]").click()
    logged_in_driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    items = logged_in_driver.find_elements(By.CLASS_NAME, "cart_item")
    screenshot_path = screenshots_dir / 'producto_ss.png'
    logged_in_driver.save_screenshot(str(screenshot_path))
    time.sleep(1)
    assert len(items) > 0