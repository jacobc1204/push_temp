# scrape a weather website for the temperature and tell me if i should wear a coat

from pushover import Client
import requests
from bs4 import BeautifulSoup

client = Client(<'your user id from pushover'>, api_token=<'your api token from pushover'>)       # sets up the pushover client

location = input('Where are you? ')                            # getting your location to search for the weather in your area

url = ('https://weather.com/weather/today/l/' + location)                # the weather website i will be using to get my info
page = requests.get(url)                                                # getting the html for that web page

soup = BeautifulSoup(page.text, 'html.parser')                          # parses the html from the website
temp = soup.find(class_='today_nowcard-temp').text                      # finds the temperature
tempnum = temp.strip('\xb0')                                            # stripping the degree symbol from the temperature

phrase = soup.find(class_='today_nowcard-phrase').text                  # finds the phrase for how the weather is
tod = soup.find(class_='today-daypart-title').text                      # finds what time of day the forecast is for

with open('push_temp.txt', 'w') as push:                                # opens a text file to write the message to

    push.write('For zipcode ' + location + ':' + '\n')                                               # specifying the location for the update
    push.write('The weather will be ' + phrase.lower() + ' ' + tod.lower() + '.\n')           # writing the forecast as the first line in the msg
    push.write('The temperature is ' + str(temp) + '.\n')                   # writing the temperature as the second line

    if int(tempnum) <= 0:                                           # depending on what the temp is
        push.write('Stay inside if you can.')                     #
    elif int(tempnum) <= 55:                                        #
        push.write('You should wear a coat.')                     # determines if you should wear a coat
    elif int(tempnum) >= 110:                                       #
        push.write('Just accept your fate.')                      #
    elif int(tempnum) >= 70:                                        # and writes it as the third line in the msg
        push.write('You should wear shorts and a tank top.')
    else:
        push.write('It will be comfortable outside today. Wear what you want.')

with open('push_temp.txt', 'r') as push:                        # opens the text file again to get the msg
    notif = push.read()

client.send_message(notif, title='Weather Update')          # sends the msg as a pushover notification
