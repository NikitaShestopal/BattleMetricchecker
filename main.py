import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import time
import asyncio

# --- НАЛАШТУВАННЯ ---
TOKEN = "8740813670:AAGksEq_ZZRu5kSEVmX5lliQ5Xbn6szAVY4"
URLS = [
    "https://www.battlemetrics.com/players/46354742",
    "https://www.battlemetrics.com/players/974641218",
    "https://www.battlemetrics.com/players/1161328175",
    "https://www.battlemetrics.com/players/1016982998"
]


def get_all_statuses():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    driver = uc.Chrome(options=options, version_main=144)
    results = []

    try:
        for url in URLS:
            driver.get(url)
            time.sleep(4)

            try:
                name = driver.find_element(By.TAG_NAME, "h1").text.replace(" Overview", "").strip()
                if "battlemetrics" in name.lower() or not name:
                    name = f"ID:{url.split('/')[-1]}"
            except:
                name = f"ID:{url.split('/')[-1]}"

            server = "Offline"
            try:
                if "Current Server(s)" in driver.page_source:
                    header = driver.find_element(By.XPATH, "//dt[contains(text(), 'Current Server(s)')]")
                    status_element = header.find_element(By.XPATH, "./following-sibling::dd")
                    val = status_element.text.strip()
                    if val and "Not online" not in val:
                        server = val
            except:
                pass

            results.append(f"👤 **{name}**\n🌐 BattleMetrics\n📊 Статус: `{server}`\n")

    finally:
        driver.quit()

    return results


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Напиши /status, щоб отримати актуальну інфу по гравцях.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("🔍 Збираю дані з BattleMetrics... Зачекай ~20-30 сек.")

    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(None, get_all_statuses)

    full_text = "📋 **Актуальний статус:**\n\n" + "\n".join(results)
    await msg.edit_text(full_text, parse_mode='Markdown')


if __name__ == '__main__':
    print("🤖 Бот запущений і чекає на команди...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    app.run_polling()