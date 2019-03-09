import discord
from discord.ext import commands
from commands.botclever import Clever
from commands import basewrapper
from boto.s3.connection import S3Connection
import os

TOKEN = os.environ.get('TOKEN')

client = commands.Bot(command_prefix="-")
client.remove_command('help')

client.listcogs = [
    "commands.botclever",
    "commands.misc",
    "commands.spotify",
    "commands.reddit"
]


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #if message.content.startswith(f"-convo"):
            #results = await client.

    if "fuck" in message.content.lower():
        """
            Idea by Nickishero
        """
        await client.send_message(message.channel, f"{message.author.mention} This is a christian server!")
        return

    if r"https://discord.gg/" in message.content.lower():
        await client.delete_message(message)
        await client.send_message(message.channel, f"{message.author.mention} No advertizing other discord servers! (If you belive this message is an error, then contact PotatoTurtle#1337)")
        return


    if message.content.startswith(f"<@{client.user.id}>"):
        basewrapper.Base().info_logger(message.content)
        results = await client.clever_response(message.content[22:])
        await client.send_message(message.channel, f"{message.author.mention} {results}")
        basewrapper.Base().info_logger("Cleverbot: " + results)
        return

    await client.process_commands(message)

@client.event
async def on_server_join():
    return

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