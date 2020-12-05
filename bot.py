import os
import random
import json
import re
from urllib.request import urlopen
from datetime import datetime, date
from bs4 import BeautifulSoup
from .credentials import token


import discord
from discord.ext import commands


TOKEN = token

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    triggered = False

    trigger_words = ["creed", "scott", "stapp", "higher"]

    for trigger in trigger_words:
        if trigger in message.content.lower():
            triggered = True

    if triggered:
        print(
            f"Creed was mentioned on {date.today().strftime('%m/%d/%y')} at {datetime.now().strftime('%H:%M:%S')}")

        song_titles_parameterized = [
            "AreYouReady",
            "WithArmsWideOpen",
            "Beautiful",
            "Bullets",
            "DontStopDancing",
            "ImEighteen",
            "FacelessMan",
            "FreedomFighter",
            "Hide",
            "Higher",
            "Illusion",
            "InAmerica",
            "InsideUsAll",
            "IsThisTheEnd",
            "Lullaby",
            "MyOwnPrison",
            "MySacrifice",
            "NeverDie",
            "Ode",
            "One",
            "OneLastBreath",
            "PityForADime",
            "SayI",
            "Signs",
            "Sister",
            "StandHereWithMe",
            "ToWhomItMayConcern",
            "Torn",
            "Unforgiven",
            "WashAwayThoseYears",
            "Weathered",
            "WhatIf",
            "WhatsThisLifeFor",
            "WhosGotMyBack",
            "WithArmsWideOpen",
            "WrongWay",
            "YoungGrowOld",
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

        song_title = str(random.choice(song_titles_parameterized))

        try:
            json_object = json.load(open('./song_info.json'))
            song_info = json_object[song_title]

            song_lyrics_unparsed = song_info["lyrics"].split("\n")
            song_lyrics = []
            for lyric in song_lyrics_unparsed:
                if lyric != "":
                    song_lyrics.append(lyric)

            song_lyric = random.choice(song_lyrics)
            song_lyric.replace("<i>", "*").replace("</i>", "*")

            color = int("%06x" % random.randint(0, 0xFFFFFF), 16)
            embed = discord.Embed(
                title="Random Creed Lyric!", description="A randomly generated Creed lyric", color=color)
            embed.add_field(
                name="Album", value=f"{song_info['album']} ({song_info['date']})", inline=False)
            embed.add_field(
                name="Song", value=song_info['real_title'], inline=False)
            embed.add_field(name="Lyric", value=song_lyric, inline=False)

            base_image_url = "http://stappsworld.com/albumart/"
            if song_info['album'] == "Weathered":
                choice = random.randint(1, 100)
                if choice > 94:
                    embed.set_image(url=f"{base_image_url}Weathered_Sam.jpg")
                else:
                    embed.set_image(url=f"{base_image_url}Weathered.jpg")
            else:
                image_url = f"{base_image_url}{song_info['album'].replace(':', '').replace(' ', '%20')}.jpg"
                embed.set_image(url=image_url)

            await message.channel.send(embed=embed)
        except Exception as e:
            print(f"{e}, song_info is : {song_title} - {song_lyric}")
            await message.channel.send(f"There was an error! ({e}) Please tell Sam!")


client.run(TOKEN)
