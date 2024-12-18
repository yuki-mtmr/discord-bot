import discord
import re
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
result = llm.invoke("Write a ballad about LangChain")
print(result.content)

intents = discord.Intents.all()
intents.message_content = True
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
