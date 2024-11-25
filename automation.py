import requests
import time
import json
import paho.mqtt.client as mqtt
from bs4 import BeautifulSoup

MQTT_HOST = "mqtt.flespi.io"
MQTT_PORT = 1883
MQTT_TOPIC = "ahmet_rytus"
MQTT_USERNAME = "FlespiToken iTxx0KnK6DtbaPmXGjKlleTQWHBtZ1v7JSszsD7m4qm33yQAFoLQqsucZVwOLRJk"
MQTT_PASSWORD = ""

TOKEN = 'RytusWebCookie=CfDJ8Mux6bliV3VGvK0McIw0514KbqxLN66aC7iVHZx6LdLFP4SbhPYDgqq9iKLNMWZei3n1PGi74tndFPoAwNN0naTRtk_4VsAMu57K-0xpePp3vAe9UMzRTyitpVyYZGJw6p4uPKlaGJPCu-HiCOXJ4HaiB1K7hQXC-Bj7Ecd6lZcYutqXGbjDRX8Lv69GIiUHbmxingk6ryYfh6QqqYblI6z41TmHX1M6LXkDOYM7U699kpXorIIAEgrdmZxW59qBxrv8uak6ph8Q9TZiyFgBDRIlaQGp5OhNR3tztDLO6KzKQxKeJPU1wTL986SGq1IqoEpWMy4gs-JiEsNUVgiKDfLKgQWSMGJgcwomABhHUp1QF7uhprlOd0BDtv6Xl4ENr1Jp_-c8QFKPSXhkTEbrjrf9-bkOYDFRIo_gStKyRdd5RKo27cuAcmDJWZQb5Y1fnxf2KRQa6gYLIhJuerjFhBLjSsc8-W2xh0Ygze9fQD9Vor72K5xuVWAz_VSMPnAN_tn9XuE_Aj2Ds7gxJlXOYFmEJ8eWSnmEl1ydTOLhRprOwczHvR_Ji202ikJOuKOrYbd0FuM7dTkw42SvInvhCFJqpXDPhMo0IvYKBEp5ACNlw90wsxSN52DiD6osFic5KIjoscZIr_dZXtS6bWtTtSBg6k6VQP2D-Vv0MrK5LL97gO0Kbp9gT4sG7fuJrmsiM3qrxGSeZpAIqmghiBZpJRmkqotrUGBlsRJL3LnuJ_pgrcsw1mQhAPS10GbAMjFbs1JAVRRzthmzcRf-NXT3PvQ; expires=Tue, 20 Aug 2024 13:25:19 GMT; path=/; secure; samesite=lax; httponly'
ANTI_FORGERY = ".AspNetCore.Antiforgery.eLO3TZKpLo0=CfDJ8Mux6bliV3VGvK0McIw0514YhaRNTETfT0N8XgE17fi5tcWesEkFRjUg8nVBoaS0T-SJFjEfXnmp6XBFkzjdXZt4C42Tlw_Cqq42_-cX8D1nNRkvh8T5LlGk2x0UOKIXrq2YEUF1cEKKpc77f-GRkh8"

ALLOWED_VALUES=['../app-assets/images/icons/alert-ok.png', '../app-assets/images/icons/alert-uparrow.jpg']

def get_token():
    url = "https://www.rytustr.com/Account/Login"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": ANTI_FORGERY,
        "origin": "https://www.rytustr.com",
        "priority": "u=0, i",
        "referer": "https://www.rytustr.com/Account/Login",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    data = {
        "username": "numberone",
        "password": "AQ24QZRuqBp",
        "__RequestVerificationToken": "CfDJ8Mux6bliV3VGvK0McIw0516fyHGJ3BZmWuu3i46h5W-M4OmDgfXx5NdQDeQsyiJvv1-PuARzhmjtDnoKfbQj8CoN9yUAnmpBtyayqYjsWNlZJqzM_H-dDUMEwL_DpTP44M3DF-07zbsMDSKaQAJTjEs"
    }

    response = requests.post(url, headers=headers, data=data, allow_redirects=False)
    return response.headers['set-cookie']

def get_data():
    url = "https://www.rytustr.com/Dashboard/TerminalStatusList"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7,ru-RU;q=0.6,ru;q=0.5",
        "cookie": ANTI_FORGERY + "; " + TOKEN,
        "priority": "u=0, i",
        "referer": "https://www.rytustr.com/Dashboard/TerminalStatusList",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    return response.text

def check_data(data):
    alerts=[]
    soup = BeautifulSoup(data, 'html.parser')
    tbody = soup.find('tbody')
    for tr in tbody.find_all('tr'):
        error_count = 0
        alert_list = []
        cells = tr.find_all('td')

        city = cells[0].text.strip()
        radio_name = cells[1].text.strip()
        freq = cells[2].text.strip()

        mpx = cells[3].find('img')['src']
        L = cells[4].find('img')['src']
        R = cells[5].find('img')['src']
        pilot = cells[6].find('img')['src']
        RDS = cells[7].find('img')['src']
        RF = cells[8].find('img')['src']
        
        if mpx not in ALLOWED_VALUES:
            #alert_list.append({'city': city, 'radio_name': radio_name, 'freq': freq, 'mpx': mpx.split('/')[-1].split('.')[0]})
            alert_list.append('(' + city + ', ' + radio_name + ', ' + freq + ', mpx, ' + mpx.split('/')[-1].split('.')[0] + ')')
            error_count += 1
        if L not in ALLOWED_VALUES:
            #alert_list.append({'city': city, 'radio_name': radio_name, 'freq': freq, 'L': L.split('/')[-1].split('.')[0]})
            alert_list.append('(' + city + ', ' + radio_name + ', ' + freq + ', L, ' + L.split('/')[-1].split('.')[0] + ')')
            error_count += 1
        if R not in ALLOWED_VALUES:
            #alert_list.append({'city': city, 'radio_name': radio_name, 'freq': freq, 'R': R.split('/')[-1].split('.')[0]})
            alert_list.append('(' + city + ', ' + radio_name + ', ' + freq + ', R, ' + R.split('/')[-1].split('.')[0] + ')')
            error_count += 1
        if pilot not in ALLOWED_VALUES:
            #alert_list.append({'city': city, 'radio_name': radio_name, 'freq': freq, 'pilot': pilot.split('/')[-1].split('.')[0]})
            alert_list.append('(' + city + ', ' + radio_name + ', ' + freq + ', pilot, ' + pilot.split('/')[-1].split('.')[0] + ')')
            error_count += 1
        if RDS not in ALLOWED_VALUES:
            #alert_list.append({'city': city, 'radio_name': radio_name, 'freq': freq, 'RDS': RDS.split('/')[-1].split('.')[0]})
            alert_list.append('(' + city + ', ' + radio_name + ', ' + freq + ', RDS, ' + RDS.split('/')[-1].split('.')[0] + ')')
            error_count += 1
        if RF not in ALLOWED_VALUES:
            #alert_list.append({'city': city, 'radio_name': radio_name, 'freq': freq, 'RF': RF.split('/')[-1].split('.')[0]})
            alert_list.append('(' + city + ', ' + radio_name + ', ' + freq + ', RF, ' + RF.split('/')[-1].split('.')[0] + ')')
            error_count += 1
        
        if error_count == 6:
            #alerts += alert_list
            alerts.append('(' + city + ', ' + radio_name + ', ' + freq + ')')

    return alerts

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        try:   
            print(f"Unexpected disconnection from MQTT broker. Reason code: {rc}")
            print("Trying to reconnect in 5 seconds...")
            time.sleep(5)
            client.reconnect()
        except Exception as e:
            print("MQTT Connect Exception: " + str(e))
            pass

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_start()

while True:
    try:
        if TOKEN == None:
            TOKEN = get_token()
        
        data = get_data()
        faulty_records = check_data(data)
        if len(faulty_records) > 0:
            client.publish(MQTT_TOPIC, json.dumps(faulty_records, ensure_ascii=False).encode('utf8'))
            print(json.dumps(faulty_records, ensure_ascii=False).encode('utf8'))
        time.sleep(60)
    except Exception as e:
        TOKEN = get_token()
        time.sleep(10)