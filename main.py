import requests
from bs4 import BeautifulSoup
from spotify import Spotify

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")


response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
chart = response.text
soup = BeautifulSoup(chart, "html.parser")
data_song = soup.find_all(name="li", class_="lrv-u-width-100p")

list_track = []

for data in data_song[::2]:
    list_track.append({
        "artist": data.find("span").getText().strip("\n""\t"),
        "track": data.find("h3").getText().strip("\n""\t")
    })

sp = Spotify(date=date, list_track=list_track)
