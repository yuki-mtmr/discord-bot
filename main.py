import discord
from discord import Game
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# GenerationConfigを使用してモデルを初期化
generation_config = genai.GenerationConfig(
    temperature=0.7,
    max_output_tokens=100,
    top_p=0.9
)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    generation_config=generation_config
)
chat = model.start_chat(history=[])

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)


def split_text(text, chunk_size=1500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=Game(name="KK"))


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author == client.user:
        return
    if message.content.startswith('KK'):
        await message.channel.send("KZM")
        input_text = message.content[2:].strip()  # "KK" プレフィックスを削除

        # プロンプトに指示を追加してモデルに送信
        prompt = (
            f"{input_text}\n\n"
            "上記に対する回答を50文字以上で作成し、最後に質問を追加してください。"
        )
        response = chat.send_message(prompt)
        answer_text = response.text

        # 応答の文字数を確認し、50文字未満の場合は再生成または追加処理を実行
        if len(answer_text) < 50:
            # ここで再生成や追加処理を実装
            answer_text += " ところで、あなたの意見はどう思いますか？"

        splitted_text = split_text(answer_text)
        for chunk in splitted_text:
            await message.channel.send(chunk)

client.run(DISCORD_BOT_TOKEN)
