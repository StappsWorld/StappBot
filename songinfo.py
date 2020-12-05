import os
import random
import json
import re
from urllib.request import urlopen
from datetime import datetime, date
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)


def write_json(data, filename='./full_circle.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def get_song_info(artist, title):
    print(f"Attempting to get {title}")
    artist = artist.lower()
    song_title = title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    # remove starting 'the' from artist e.g. the who -> who
    if artist.startswith("the"):
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"

    try:
        driver.get(url)

        lyrics = get_lyrics()

        # album name and date
        album_div = driver.find_element_by_class_name("songinalbum_title")
        album_b = album_div.find_element_by_xpath('./b')
        album_name = album_b.text.replace('<br>', '').replace(
            '</br>', '').replace('</div>', '').replace('"', '').strip()
        date_text = album_div.text.split("(")[1].split(")")[0]
        album_date = int(date_text)

        # song title
        song_full_title = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/b").text.replace(
            '<br>', '').replace('</br>', '').replace('</div>', '').replace('"', '').strip()

        return {"album": album_name, "date": album_date, "real_title": song_full_title, "lyrics": lyrics}
    except Exception as e:
        return [f"exception {e}", lyrics]


def get_lyrics():
    try:
        lyrics = driver.page_source
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>', '').replace(
            '</br>', '').replace('</div>', '').strip()

        return lyrics
    except Exception as e:
        return f"lyrics failed {e}"


song_titles_parameterized = [
    "Bread Of Shame",
    "A Thousand Faces",
    "Suddenly",
    "Rain",
    "Away In Silence",
    "Fear",
    "On My Sleeve",
    "Full Circle",
    "Time",
    "Good Fight",
    "The Song You Sing",
    "Silent Teacher",
]

valid = []
error = []
to_be_written = {}

for title in song_titles_parameterized:
    returned = get_song_info("creed", title)
    if type(returned) == list:
        error.append(title)
        write = {title: "to be filled"}
    else:
        valid.append(returned)
        write = returned
    to_be_written[title] = write
    print(write)

driver.close()

print(f"There were errors: {error}")

write_json(to_be_written)
