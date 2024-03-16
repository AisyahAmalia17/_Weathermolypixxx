import telebot
import requests
import datetime
from geopy.geocoders import Nominatim
from dotenv import dotenv_values


# Define bot and weather API tokens
env = dotenv_values(".env")
BOT_TOKEN = env['BOT_TOKEN']
WEATHER_TOKEN = env['WEATHER_TOKEN']
POLLING_TIMEOUT = None
bot = telebot.TeleBot(BOT_TOKEN)
bot.set_webhook()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Just click /weather and send  your location or ask for the forecast. Hope it helps you 🤗🌈✨')


@bot.message_handler(commands=['weather'])
def send_weather(message):
    location = 'Enter a Location: '
    sent_message = bot.send_message(message.chat.id, location, parse_mode='Markdown')
    bot.register_next_step_handler(sent_message, fetch_info)
    return location


def location_handler(message):
    location = message.text
    geolocator = Nominatim(user_agent="my_app")
    print(geolocator)

    try:
        location_data = geolocator.geocode(location)
        print (location_data)
        latitude = round(location_data.latitude,2)
        longitude = round(location_data.longitude,2)
        return latitude, longitude
    except (AttributeError):
        print("Location not found.")


def get_weather(latitude,longitude):
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&appid={}'.format(latitude, longitude, WEATHER_TOKEN)
    response = requests.get(url)
    return response.json()


def fetch_info(message): 
    try:
        latitude, longitude = location_handler(message)
        
        weather = get_weather(latitude,longitude)
        data = weather['list']
        data_2 = data[0]

        info = data_2['weather']
        data_3 = info[0]
        main = data_3['main']

        info = data_2['weather']
        data_3 = info[0]
        description = data_3['description'].capitalize()

        dt_txt = data_2['dt_txt']
        dt = datetime.datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
        formatted_date_time = dt.strftime('%A, %B %d, %Y %I:%M %p %Z')

        info = data_2['main']
        temp = info['temp']

        info = data_2['main']
        feels_like = info['feels_like']

        info = data_2['main']
        temp_max = info['temp_max']

        info = data_2['main']
        temp_min = info['temp_min']

        info = data_2['wind']
        speed = info['speed']

        info = data_2['wind']
        deg = info['deg']

        info = data_2['clouds']
        all = info['all']

        
        weather_message = f'*Weather:* {main} - {description}\n\n*Temperature:* {temp:.2f}°C\n    *Feels_Like:* {feels_like:.2f}°C\n    *Max Temp:* {temp_max:.2f}°C\n    *Min Temp:* {temp_min:.2f}°C\n\nWind \n    *Wind Speed:* {speed}m/s\n    *Wind Degree:* {deg}°\n\n *Cloudiness:* {all}% \n\n*Weather info updated on:*\n{formatted_date_time}\n'
        bot.send_message(message.chat.id, 'Here\'s the weather!')
        bot.send_message(message.chat.id, weather_message, parse_mode='Markdown')

    except TypeError:
        bot.send_message(message.chat.id, 'Please enter the valid location')
            
print('Starting bot...')
print('Polling...') 
bot.infinity_polling()