import json
from flask import Flask
app = Flask(__name__)

countries = [{'id': 1, 'name': 'Turkey'},{'id': 2, 'name': 'Russia'},{'id': 3, 'name': 'Ukraine'}]

@app.route('/verify/<answer>')
def verify(answer):
    return True

@app.route('/country_list')
def country_list():
    return json.dumps(countries)

@app.route('/question/<int:country_id>')
def question(country_id):
    question = {}
    if country_id == 1:
        question['url'] = 'https://www.google.com/maps/@38.7207494,35.4823757,3a,75y,88.09h,92.6t/data=!3m7!1e1!3m5!1sJ4YsSn9Um_0Y_YKK82x26A!2e0!6s%2F%2Fgeo2.ggpht.com%2Fcbk%3Fpanoid%3DJ4YsSn9Um_0Y_YKK82x26A%26output%3Dthumbnail%26cb_client%3Dmaps_sv.tactile.gps%26thumb%3D2%26w%3D203%26h%3D100%26yaw%3D11.282314%26pitch%3D0%26thumbfov%3D100!7i16384!8i8192'
        question['options'] = [{'id':10, 'name': 'Kayseri'}, {'id':11, 'name': 'Adana'}, {'id':12, 'name': 'İstanbul'}, {'id':13, 'name': 'Bartın'}, {'id':14, 'name': 'Yalova'}]
        question['text'] = 'Burası hangi şehir?'
    elif country_id == 2:
        question['url'] = 'https://www.google.com/maps/@55.7537707,37.6220942,2a,75y,285.61h,92.62t/data=!3m6!1e1!3m4!1swi-G1Ke9J0948AKcnQhuZw!2e0!7i13312!8i6656'
        question['options'] = [{'id':15, 'name': 'Moscow'}, {'id':16, 'name': 'Saint Petersburg'}, {'id':17, 'name': 'Novosibirsk'}, {'id':18, 'name': 'Yekaterinburg'}, {'id':19, 'name': 'Kazan'}]
        question['text'] = 'Burası hangi şehir?'
    elif country_id == 3:
        question['url'] = 'https://www.google.com/maps/@48.4623681,35.0758052,3a,75y,352.68h,88.68t/data=!3m8!1e1!3m6!1sAF1QipOGoxXl9yKwosMlte3sv0L-LXMJuJfV1Fdnr-6-!2e10!3e11!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2FAF1QipOGoxXl9yKwosMlte3sv0L-LXMJuJfV1Fdnr-6-%3Dw203-h100-k-no-pi0-ya278.66345-ro-0-fo100!7i8000!8i4000'
        question['options'] = [{'id':20, 'name': 'Kyiv'}, {'id':21, 'name': 'Kharkiv'}, {'id':22, 'name': 'Odessa'}, {'id':23, 'name': 'Dnipro'}, {'id':24, 'name': 'Donetsk'}]
        question['text'] = 'Burası hangi şehir?'
    return json.dumps(question)

if __name__ == '__main__':
   app.run()


# no input - ülke listesi 
# input ülke ismi - şehir sorusu
