from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Настройки Selenium
options = Options()
#options.add_argument("--headless")  # Запуск без графического интерфейса
#options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Запуск драйвера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# URL страницы
url = "https://www.avito.ru/irkutsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA&district=390&f=ASgBAgICAkSSA8YQkL4Nlq41"
driver.get(url)
time.sleep(5)  # Ждём загрузки страницы

# Загружаем cookies
with open("avito_cookies.json", "r") as file:
    cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

driver.refresh()  # Обновляем страницу, чтобы cookies применились
time.sleep(3)

# Проверяем, авторизовались ли мы
if "Профиль" in driver.page_source:
    print("Авторизация успешна!")
else:
    print("Ошибка авторизации!")

# Дальше можно запускать ваш парсер

# Список объявлений
listings = driver.find_elements(By.XPATH, "//div[contains(@data-marker, 'item')]//a[@itemprop='url']")

results = []

for i in range(len(listings)):
    try:
        # Повторное нахождение элемента, чтобы избежать StaleElementException
        listings = driver.find_elements(By.XPATH, "//div[contains(@data-marker, 'item')]//a[@itemprop='url']")
        link = listings[i].get_attribute("href")
        driver.get(link)
        time.sleep(3)

        wait = WebDriverWait(driver, 10)

        # Название объявления
        title = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[@itemprop='name']"))).text.strip()

        # Адрес
        street = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-marker='street_link']"))).text.strip()
        house = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-marker='house_link']"))).text.strip()
        address = f"{street}, {house}"

        # Имя продавца
        seller_name = wait.until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'styles-module-size_s')]"))).text.strip()

        # Ссылка на профиль продавца
        seller_profile_link = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@data-marker, 'seller-link')]"))).get_attribute(
            "href")

        results.append({
            "title": title,
            "address": address,
            "seller_name": seller_name,
            "seller_profile": seller_profile_link
        })

        # Возвращаемся назад
        driver.get(url)
        time.sleep(3)

    except Exception as e:
        print(f"Ошибка обработки объявления: {e}")
        continue

# Закрываем браузер
driver.quit()

# Вывод результатов
for res in results:
    print(res)
