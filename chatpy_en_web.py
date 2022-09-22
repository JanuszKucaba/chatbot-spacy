import spacy
import requests
from flask import Flask, render_template, request


api_key = 'f09032aeb69832cb32cbad04bee188c9'

app = Flask(__name__)
nlp = spacy.load('pl_core_news_sm')

topic = nlp('temperatura w mieście')
exit_conditions = nlp('Koniec rozmowy')


def display_weather_temperature(city):
    open_weather_url = f'http://api.openweathermap.org/data/2.5/weather/?appid={api_key}&q={city}&units=metric'
    response = requests.get(open_weather_url)
    temperature = response.json()['main']['temp']
    print(f'W {city} jest {temperature} C')


def handle_user_input(user_input):
    # Convert the user text input into NLP document
    user_input = nlp(user_input)
    print(user_input)

    # Checking the threshold
    if user_input.similarity(topic) >= 0.60:
        for ent in user_input.ents:     # Checkinh the entities
            if ent.label_ == 'GPE':     # Veryfiying if its is a geographical Entity
                city = ent.text
                return display_weather_temperature(city)
            else:
                return ('Przepraszam, ale nie wykrywam lokalizacji. Proszę spróbuj zapytać o coś innego.')
    else:
        if user_input.similarity(exit_conditions) >= 0.70:
            return 'Ok, do zobaczenia.'
        else:
            return 'Przepraszam, ale nie rozumiem tego. Proszę spróbuj zapytać o coś innego.'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get')
def bot_response():
    user_message = request.args.get('msg')
    return str(handle_user_input(user_message))


if __name__ == '__main__':
    app.run(debug=True)
