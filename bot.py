'''RUN THIS FILE ONLY AFTER RUNNING server.py'''

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
import os


load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    try:
     
        await message.channel.trigger_typing()
        res = requests.get("http://localhost:5001/chat?q=" + message.content)
        await message.channel.send(res.text)
    except:
        await message.channel.send("Somehting went wrong. Make sure you have logged in with your GPT3 account")


client.run(
    DISCORD_BOT_TOKEN)
