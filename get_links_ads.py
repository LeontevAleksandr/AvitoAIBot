from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Настройка Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск без окна браузера
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ссылка на страницу
#url = "https://www.avito.ru/irkutsk/kvartiry/prodam-ASgBAgICAUSSA8YQ"
url = "https://www.avito.ru/irkutsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA&f=ASgBAgICAkSSA8YQkL4Nlq41"

driver.get(url) # Открываем страницу
time.sleep(3)  # Даем время на загрузку

page = 1
counter_ads = 1

with open("avito_links.txt", "w", encoding="utf-8") as file:
    file.write("") # Очищаем файл перед началом работы

print("Сбор объявлений")
while True:
    print(f"Собираем данные с {page}-й страницы...")
    ads = driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')  # Получаем все объявления на странице

    with open("avito_links.txt", "a", encoding="utf-8") as file:  # Запись в файл
        for ad in ads:
            try:
                ad_link = ad.find_element(By.TAG_NAME, "a").get_attribute("href")
                print(f"Ссылка на объявление {counter_ads}:", ad_link)
                file.write(ad_link + "\n")
                counter_ads += 1
            except Exception as e:
                print(f"Ошибка: {e}")
                continue

    try: # Проверяем, есть ли кнопка "Следующая страница"
        next_page_button = driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]')
        next_page_button.click()
        page += 1
        time.sleep(5)  # Даем время на загрузку новой страницы
    except Exception as errorPage:
        print(f"Следующей страницы нет, завершаем работу. {errorPage}")
        break

print("Ссылки сохранены в avito_links.txt.")

driver.quit() # Закрываем браузер
