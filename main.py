import discord
from discord import Game
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')
chat = model.start_chat(history=[])

intents = discord.Intents.all()
intents.message_content = True
discord = discord.Client(intents=intents)


def split_text(text, chunk_size=1500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


@discord.event
async def on_ready():
    print(f'We have logged in as {discord.user}')
    await discord.change_presence(activity=Game(name="任意の文字列"))


@discord.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author == discord.user:
        return
    await message.channel.send("---")
    input_text = message.content

    answer = chat.send_message(input_text)

    splitted_text = split_text(answer.text)
    for chunk in splitted_text:
        await message.channel.send(chunk)

discord.run(DISCORD_BOT_TOKEN)
