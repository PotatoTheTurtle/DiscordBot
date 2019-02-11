import discord
from discord.ext import commands
from commands.botclever import Clever
from datetime import datetime


TOKEN = 
time = datetime.today()
client = commands.Bot(command_prefix="!")

client.listcogs = [
    "commands.botclever",
    "commands.misc",
    "commands.spotify"
]


def info_logger(message):
    print(f"[{time} - INFO] {message}")


def error_logger():
    raise Exception(f"[{time} - **ERROR**] {message}")


def warning_logger():
    print(f"[{time} - *WARNING*] {message}")


@client.event
async def on_message(message):
    if message.content.startswith(f"<@{client.user.id}>") and message.author != client.user:
        info_logger(message.content)
        results = await client.clever_response(message.content[22:])
        await client.send_message(message.channel, f"{message.author.mention} {results}")
        info_logger("Cleverbot: " + results)
        return

    await client.process_commands(message)


@client.event
async def on_ready():
    print('INIT')
    print(client.user.name)
    print(client.user.id)
    print("---------")
    for cog in client.listcogs:
        try:
            client.load_extension(cog)
            print(f"Loaded sucessfully: {cog}")
        except Exception as e:
            print(f"Failed to load: {cog}, error: {e}")

    print('END - BOT STARTED')


client.run(TOKEN)