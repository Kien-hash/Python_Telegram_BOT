import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Thay thế bằng token Telegram của bạn
TELEGRAM_BOT_TOKEN = '7871310922:AAFUSA54ANVvUzM57xuD4OU02LtqzpkIpA8'
# Thay thế bằng API Key từ OpenWeatherMap
WEATHER_API_KEY = '92c1dae6e1a229c88104875516085368'

def get_international_gold_price():
    api_key = "goldapi-19oa2sm2z2uu45-io"  # Thay bằng API Key của bạn
    symbol = "XAU"
    curr = "USD"
    date = ""  # Nếu cần lấy dữ liệu ngày cụ thể, thêm ngày theo định dạng: /YYYY-MM-DD

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"
    
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        
        # Kiểm tra dữ liệu và định dạng lại cho dễ đọc
        if data.get("metal") and data.get("price"):
            gold_price = data["price"]
            time_stamp = data["timestamp"]
            currency = data["currency"]
            metal = data["metal"]

            # Định dạng thông tin giá vàng
            formatted_response = (
                f"Thông tin giá vàng quốc tế:\n"
                f"- Kim loại: {metal}\n"
                f"- Giá: {gold_price} {currency}/ounce\n"
                f"- Thời gian cập nhật: {time_stamp}"
            )
        else:
            formatted_response = "Không thể lấy thông tin giá vàng. Vui lòng kiểm tra API Key hoặc tham số."

        return formatted_response

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"



# Hàm để lấy thông tin thời tiết
def get_weather(city):
    print(city)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=vi"
    response = requests.get(url)
    data = response.json()
    print(response)
    if response.status_code == 200:
        weather_description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        
        return (
            f"Thời tiết ở {city.capitalize()}:\n"
            f"- Mô tả: {weather_description.capitalize()}\n"
            f"- Nhiệt độ: {temp}°C (cảm giác như {feels_like}°C)\n"
            f"- Độ ẩm: {humidity}%"
        )
    else:
        return "Không thể lấy thông tin thời tiết. Vui lòng kiểm tra tên thành phố."

# Hàm để xử lý lệnh /weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Kiểm tra xem người dùng có nhập tên thành phố không
    if len(context.args) == 0:
        city = "Hanoi"  # Thành phố mặc định
        await update.message.reply_text("Bạn chưa nhập thành phố. Sử dụng mặc định: Hà Nội")
    else:
        city = " ".join(context.args)  # Nối các từ lại thành tên thành phố

    # In ra các tham số để kiểm tra
    print("City:", city)
    
    # Lấy thông tin thời tiết
    weather_info = get_weather(city)
    print("Weather info:", weather_info)  # In thông tin thời tiết nhận được từ API

    # Trả lời người dùng
    await update.message.reply_text(weather_info)

async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    gold_price_info = get_international_gold_price()
    await update.message.reply_text(gold_price_info)


# Cấu hình bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Đăng ký lệnh /weather
    application.add_handler(CommandHandler("thoitiet", weather))

    application.add_handler(CommandHandler("vang", gold))


    # Khởi động bot
    application.run_polling()

if __name__ == '__main__':
    print("Running...")
    main()
    print("Finished!")
