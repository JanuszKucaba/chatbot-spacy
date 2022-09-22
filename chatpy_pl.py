import requests
import spacy

from deep_translator import GoogleTranslator


api_key = 'f09032aeb69832cb32cbad04bee188c9'

nlp = spacy.load('pl_core_news_sm')
topic = nlp('stan pogody w mieście')

user_input = input('Cześć! Jestem botem pogodowym. Jak Ci momgę pomóc ?\n')

# Convert the user text input into NLP document
user_input = nlp(user_input)


def display_weather_conditions(city):
    open_weather_url = f'http://api.openweathermap.org/data/2.5/weather/?appid={api_key}&q={city}'
    response = requests.get(open_weather_url)
    weather = response.json()['weather'][0]['description']
    trans_weather = GoogleTranslator(source='auto', target='pl').translate(weather).lower()
    print(f'Jest {trans_weather} w {city}')


# Checking the threshold
if user_input.similarity(topic) >= 0.60:
    for ent in user_input.ents:  # Checking the entities
        if ent.label_ == "GPE":  # Verifying if its a geographical Entity
            city = ent.text
            display_weather_conditions(city)
            break
        else:
            print('Przepraszam, ale nie jestem w stanie ustalić lokalizacji')
else:
    print('Przepraszam, ale nie rozumiem co napisałeś. Napisz jeszcze raz.')
