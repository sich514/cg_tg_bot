import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

API_KEY = "CG-njVjEATCk7MDzYeQ6tyxcVJ5"
TELEGRAM_BOT_TOKEN = "8584072610:AAF59ziSkZq-Xr0zorOOPk8jih4bQ8yx7is"  


# Функция получения данных с CoinGecko
def get_perp_markets(symbol: str):
    symbol = symbol.lower()
    url = "https://api.coingecko.com/api/v3/derivatives"
    r = requests.get(url, headers={"x-cg-pro-api-key": API_KEY})
    data = r.json()
    results = []

    for d in data:
        contract_type = d.get("contract_type", "").lower()
        pair = d.get("symbol", "").lower()
        if contract_type == "perpetual" and pair.startswith(symbol):
            results.append({
                "exchange": d.get("market"),
                "symbol": d.get("symbol"),
                "price": d.get("price"),
            })

    return results


# Функция для форматирования ответа
def format_markets(symbol: str):
    markets = get_perp_markets(symbol)
    if not markets:
        return f"❌{symbol.upper()} не найден"

    msg = f"Фьючерсные рынки для {symbol.upper()}:\n\n"
    for m in markets:
        msg += f"• {m['exchange']} → {m['symbol']} → ${m['price']}\n"
    return msg


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отправь мне тикер криптовалюты, например ZEС, Zec или zec, "
        "и я покажу фьючерсные рынки для него."
    )


# Обработчик сообщений с тикером
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = update.message.text.strip()
    response = format_markets(symbol)
    await update.message.reply_text(response)


# Основной запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()
