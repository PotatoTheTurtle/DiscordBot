import discord
from discord.ext import commands
from commands.botclever import Clever
from commands import basewrapper


TOKEN = 'NTQwMzAwMjY0OTg5NTIzOTgx.Dz4nzw.nTHGB0hTuDPFPp0TOvejtCK3J28'
client = commands.Bot(command_prefix="!")

client.listcogs = [
    "commands.botclever",
    "commands.misc",
    "commands.spotify"
]


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f"<@{client.user.id}>"):
        basewrapper.Base().info_logger(message.content)
        results = await client.clever_response(message.content[22:])
        await client.send_message(message.channel, f"{message.author.mention} {results}")
        basewrapper.Base().info_logger("Cleverbot: " + results)
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