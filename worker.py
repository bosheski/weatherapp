import requests
import psycopg2
import psycopg2.extras
from datetime import datetime
import logging


def collect_data():
    api_token = 'a51d959342f55372'

    url = 'http://api.wunderground.com/api/' + api_token + '/conditions/q/RS/Belgrade.json'
    r = requests.get(url).json()
    data = r['current_observation']

    location = data['observation_location']['full']     # city , state, observation location
    weather = data['weather']   # cloud, clear
    wind_string = data['wind_string']    # wind direction, speed
    temp = data['temperature_string']
    humidity = data['relative_humidity']    # humidity
    precip = data['precip_today_string']  # precip in inches and mm
    icon_url = data['icon_url']  # url for icon (clear, cloud, rainy)
    observation_time = data['observation_time']     # observation time

    # open db
    try:
        connection = psycopg2.connect(dbname='weather' , user='postgres', host='localhost', password='dino1937456')
        print('Opened Database Successfully')
    except:
        print(datetime.now(), "Unable to connect to the database")
        logging.exception("Unable to open the database")
        return
    else:
        curs = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # write data to database

    curs.execute("""INSERT INTO mainpart_reading(location, weather, wind_string, temp, humidity, precip, icon_url, observation_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (location, weather, wind_string, temp, humidity,
                                                                      precip, icon_url, observation_time))

    connection.commit()
    curs.close()
    connection.close()

    print("Data Written", datetime.now())
collect_data()
