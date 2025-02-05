from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json

options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Открываем Avito, где уже выполнен вход
driver.get("https://www.avito.ru")
input("Нажмите Enter после входа в аккаунт...")

# Сохраняем cookies
cookies = driver.get_cookies()
with open("avito_cookies.json", "w") as file:
    json.dump(cookies, file)

driver.quit()
print("Cookies сохранены в avito_cookies.json")
