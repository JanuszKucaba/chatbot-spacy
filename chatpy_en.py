import requests
import spacy


api_key = 'f09032aeb69832cb32cbad04bee188c9'

nlp = spacy.load('en_core_web_sm')
topic = nlp('Weather conditions in a city')

user_input = input('Hello, I am a weather bot. How can I help You\n')

# Convert the user text input into NLP document
user_input = nlp(user_input)


def display_weather_conditions(city):
    open_weather_url = f'http://api.openweathermap.org/data/2.5/weather/?appid={api_key}&q={city}'
    response = requests.get(open_weather_url)
    weather = response.json()['weather'][0]['description']
    print(f'Jest {weather} w {city}')


# Checking the threshold
if user_input.similarity(topic) >= 0.60:
    for ent in user_input.ents:  # Checking the entities
        if ent.label_ == "GPE":  # Verifying if its a geographical Entity
            city = ent.text
            display_weather_conditions(city)
            break
        else:
            print('Sorry I am unable to detect a location')
else:
    print('Sorry I don\'t understand that. Please rephrase your statement.')
