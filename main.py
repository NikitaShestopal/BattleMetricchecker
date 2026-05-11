import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
import os

URLS = [
    "https://www.battlemetrics.com/players/46354742",
    "https://www.battlemetrics.com/players/974641218",
    "https://www.battlemetrics.com/players/1161328175",
    "https://www.battlemetrics.com/players/1016982998"
]

DELAY_BETWEEN_CYCLES = 60
CSV_FILE = "activity_log.csv"


def log_to_csv(name, status, server):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        if not file_exists:
            writer.writerow(['Час', 'Гравець', 'Статус', 'Сервер'])

        writer.writerow([timestamp, name, status, server])

    print(f"[{timestamp}] {name}: {status} | {server}")


def check_players():
    print(f"🚀 Моніторинг запущено. Дані пишуться в {CSV_FILE}")

    while True:
        driver = None
        try:
            # ПЕРЕНЕСЕНО СЮДИ: Кожного разу створюємо нові опції
            options = uc.ChromeOptions()
            options.add_argument('--headless')
            options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

            driver = uc.Chrome(options=options, version_main=144)

            for url in URLS:
                try:
                    driver.get(url)
                    time.sleep(5)

                    try:
                        name = driver.find_element(By.TAG_NAME, "h1").text.replace(" Overview", "").strip()
                    except:
                        name = f"ID:{url.split('/')[-1]}"

                    status = "Offline"
                    server_name = "-"
                    if "Current Server(s)" in driver.page_source:
                        try:
                            header = driver.find_element(By.XPATH, "//dt[contains(text(), 'Current Server(s)')]")
                            status_element = header.find_element(By.XPATH, "./following-sibling::dd")
                            val = status_element.text.strip()
                            if val and "Not online" not in val:
                                status = "Online"
                                server_name = val
                        except:
                            pass

                    log_to_csv(name, status, server_name)

                except Exception as e:
                    print(f"❌ Помилка з {url}: {e}")

                time.sleep(2)

        except Exception as e:
            print(f"⚠️ Критична помилка браузера: {e}")

        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

        print(f"💤 Пауза {DELAY_BETWEEN_CYCLES} сек...")
        time.sleep(DELAY_BETWEEN_CYCLES)

if __name__ == '__main__':
    try:
        check_players()
    except KeyboardInterrupt:
        print("\n🛑 Зупинено.")