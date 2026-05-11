import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from datetime import datetime

URLS = [
    "https://www.battlemetrics.com/players/46354742",
    "https://www.battlemetrics.com/players/974641218",
    "https://www.battlemetrics.com/players/1161328175",
    "https://www.battlemetrics.com/players/1016982998"
]

DELAY_BETWEEN_CYCLES = 60
LOG_FILE = "activity_log.txt"


def log_to_file(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    print(full_message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_message + "\n")


def check_players():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    print(f"🚀 Запуск моніторингу... (пауза між циклами: {DELAY_BETWEEN_CYCLES} сек.)")

    while True:
        driver = None
        try:
            driver = uc.Chrome(options=options, version_main=144)

            for url in URLS:
                try:
                    driver.get(url)
                    time.sleep(5)

                    try:
                        name = driver.find_element(By.TAG_NAME, "h1").text.replace(" Overview", "").strip()
                        if "battlemetrics" in name.lower() or not name:
                            name = f"ID:{url.split('/')[-1]}"
                    except:
                        name = f"ID:{url.split('/')[-1]}"

                    server = "Offline"
                    if "Current Server(s)" in driver.page_source:
                        try:
                            header = driver.find_element(By.XPATH, "//dt[contains(text(), 'Current Server(s)')]")
                            status_element = header.find_element(By.XPATH, "./following-sibling::dd")
                            val = status_element.text.strip()
                            if val and "Not online" not in val:
                                server = val
                        except:
                            pass

                    status_text = f"ОНЛАЙН: {name} на {server}" if server != "Offline" else f"ОФЛАЙН: {name}"
                    log_to_file(status_text)

                except Exception as e:
                    print(f"❌ Помилка при перевірці {url}: {e}")

                time.sleep(2)

        except Exception as e:
            print(f"⚠️ Критична помилка браузера: {e}")

        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

        print(f"💤 Очікування {DELAY_BETWEEN_CYCLES} секунд до наступної перевірки...")
        time.sleep(DELAY_BETWEEN_CYCLES)


if __name__ == '__main__':
    try:
        check_players()
    except KeyboardInterrupt:
        print("\n🛑 Моніторинг зупинено користувачем.")