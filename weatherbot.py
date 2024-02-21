import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
TOKEN = '6959294318:AAFU4SrQ8CkavRxHLkTWecQkDyVIAIrparY'
API_KEY = 'ac6f69f3a6ebadeb9e39ac494eb38058'
URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'
EMOJI_CODE = {200: '⛈',
              201: '⛈',
              202: '⛈',
              210: '🌩',
              211: '🌩',
              212: '🌩',
              221: '🌩',
              230: '⛈',
              231: '⛈',
              232: '⛈',
              301: '🌧',
              302: '🌧',
              310: '🌧',
              311: '🌧',
              312: '🌧',
              313: '🌧',
              314: '🌧',
              321: '🌧',
              500: '🌧',
              501: '🌧',
              502: '🌧',
              503: '🌧',
              504: '🌧',
              511: '🌧',
              520: '🌧',
              521: '🌧',
              522: '🌧',
              531: '🌧',
              600: '🌨',
              601: '🌨',
              602: '🌨',
              611: '🌨',
              612: '🌨',
              613: '🌨',
              615: '🌨',
              616: '🌨',
              620: '🌨',
              621: '🌨',
              622: '🌨',
              701: '🌫',
              711: '🌫',
              721: '🌫',
              731: '🌫',
              741: '🌫',
              751: '🌫',
              761: '🌫',
              762: '🌫',
              771: '🌫',
              781: '🌫',
              800: '☀️',
              801: '🌤',
              802: '☁️',
              803: '☁️',
              804: '☁️'}

bot = telebot.TeleBot(TOKEN)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Получить погоду', request_location=True))
keyboard.add(KeyboardButton('О проекте'))

def get_weather(lat, lon):
    params = {'lat': lat,
              'lon': lon,
              'lang': 'ru',
              'units': 'metric',
              'appid': API_KEY}
    response = requests.get(url=URL_WEATHER_API, params=params).json()
    print(response)
    city_name = response['name']
    description = response['weather'][0]['description']
    code = response['weather'][0]['id']
    temp = response['main']['temp']
    temp_feels_like = response['main']['feels_like']
    humidity = response['main']['humidity']
    emoji = EMOJI_CODE[code]
    message = f'🏣 Погода в: {city_name}\n'
    message += f'{emoji} {description.capitalize()}.\n'
    message += f'🌡️ Температура {temp}°C.\n'
    message += f'💀 Ощущается {temp_feels_like}°C.\n'
    message += f'💦 Влажность {humidity}%.\n'
    return message

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = 'Отправьте мне свое местоположение, и я отправлю тебе погоду'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon = message.location.longitude
    lat = message.location.latitude
    result = get_weather(lat, lon)
    if result:
        bot.send_message(message.chat.id, result, reply_markup=keyboard)

@bot.message_handler(regexp='О проекте')
def send_about(message):
    text = 'Этот бот предназначен для получения информации о погоде в Вашем городе. Для этого Вам надо отправить необходимые данные. Автор данного бота - ученик 11 класса Шапков Гордей'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


bot.infinity_polling()