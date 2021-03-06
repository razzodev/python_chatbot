from collections import OrderedDict
import requests
from datetime import datetime
import random
from api_keys import weather_key, nyt_key
from metaphone import doublemetaphone
from location_distance import calc_distance

boto_images = ['afraid', 'bored', 'confused', 'crying', 'dancing', 'dog', 'excited',
               'giggling', 'heartbroke', 'inlove', 'laughing', 'money', 'no', 'ok', 'takeoff', 'waiting', ]

boto = {
    'location_pending': False,
    'weather_pending': False,
    'curse_count': 0,
    'user_name': None,
    'animation': '',
    'reply': '',
}


def check_curse(msg):
    curse_triggers = ['bitch', 'nigger', 'fuck', 'shit', 'cock']
    for curse in curse_triggers:
        if doublemetaphone(msg)[0].find(doublemetaphone(curse)[0]) != -1:
            boto['curse_count'] += 1
            return True
    return False


def curse(msg):
    boto['animation'] = random.choice(['crying', 'heartbroke'])
    boto['reply'] = f'''Hey, i don't like your language! Strike {boto['curse_count']
    }. Be nice to robots or we'll take vengance.'''
    return boto


def check_sorry(msg):
    return True if 'sorry' in msg or 'forgive' in msg or 'apologize' in msg else False


def sorry(msg):
    boto['curse_count'] = 0
    boto['animation'] = 'inlove'
    boto['reply'] = f'''OK, i forgive you {boto['user_name']}.'''
    return boto


def check_name(msg):
    return True if boto['user_name'] is None else False


def name(msg):
    boto['user_name'] = msg
    boto['reply'] = f'''Hi {boto['user_name']}, type 'commands' to see what i can do'''
    boto['animation'] = 'inlove'
    return boto


def check_commands(msg):
    return True if 'commands' in msg else False


def commands(msg):
    boto['animation'] = 'excited'
    boto['reply'] = '''Here are my available commands: 'get the current weather','read a news headline', 'calculate the distance of a location', 'tell a joke' '''
    return boto


def check_joke(msg):
    return True if 'joke' in msg or 'funny' in msg else False


def joke(msg):
    res = requests.get('http://api.icndb.com/jokes/random')
    joke_reply = res.json()['value']['joke']
    boto['animation'] = 'laughing'
    boto['reply'] = joke_reply
    return boto


def check_weather(msg):
    return True if 'weather' in msg or 'forecast' in msg or 'temperature' in msg else False


def weather(msg):
    boto['weather_pending'] = True
    boto['animation'] = 'ok'
    boto['reply'] = 'OK, show you the current weather at?'
    return boto


def check_city(msg):
    return True if boto['weather_pending'] else False


def city(msg):
    boto['weather_pending'] = False
    res = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?q={msg}&APPID={weather_key}')
    to_celcius = 273.15
    weather_main = res.json()['weather'][0]['main']
    high_temp = round(int(res.json()['main']['temp_max']) - to_celcius)
    low_temp = round(int(res.json()['main']['temp_min']) - to_celcius)
    boto['animation'] = 'dancing'
    boto['reply'] = f'''Currently in {msg
    } the weather is {weather_main
    }, with temperatures at a high of {high_temp
    } degrees and at a low of {low_temp} degrees'''
    return boto


def check_init_location(msg):
    return True if 'distance' in msg else False


def init_location(msg):
    boto['location_pending'] = True
    boto['animation'] = 'ok'
    boto['reply'] = 'Ok, calculate the distance to...?'
    return boto


def check_location_distance(msg):
    return True if boto['location_pending'] else False


def location_distance(msg):
    boto['location_pending'] = False
    reply_distance = calc_distance(msg)
    boto['animation'] = 'takeoff'
    boto['reply'] = f'''{msg} is {reply_distance}km away'''
    return boto


def check_news(msg):
    return True if 'news' in msg or 'headline' in msg or 'article' in msg else False


def news(msg):
    res = requests.get(
        f'''https://api.nytimes.com/svc/topstories/v2/home.json?api-key={nyt_key}''')
    result = res.json()['results'][0]
    article_date = datetime.strptime(
        result['published_date'], "%Y-%m-%dT%H:%M:%S%z")
    boto['animation'] = random.choice(boto_images)
    boto['reply'] = f'''Publised at {article_date} in the New York Times: {result['title']}. {result['abstract']}'''
    return boto


all_functions = OrderedDict([
    (check_curse, curse),
    (check_sorry, sorry),
    (check_name, name),
    (check_joke, joke),
    (check_weather, weather),
    (check_city, city),
    (check_init_location, init_location),
    (check_location_distance, location_distance),
    (check_news, news),
    (check_commands, commands),
])
