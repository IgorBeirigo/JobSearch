from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Instalar e configurar o ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Acessar um site para testar
driver.get("https://www.google.com")
input("Pressione Enter para fechar...")

# Fechar o navegador
driver.quit()
