import discord
import re
import os
from dotenv import load_dotenv

load_dotenv()

# 環境変数を取得する
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name="任意の文字列"))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author == client.user:
        return
    if message.content.startswith('hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('おもち'):
        await message.channel.send('もちもち')

client.run(DISCORD_BOT_TOKEN)
