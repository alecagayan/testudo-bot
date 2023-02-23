import discord
from discord.ext import commands
from discord.ext.commands import Bot
import config


intents = discord.Intents.default()
intents.members = True
client = Bot(description=config.des, command_prefix=config.pref, intents=intents)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.load_extension('cogs.planetterp')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

client.run(config.bbtoken)
