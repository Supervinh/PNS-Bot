import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True

bot = commands.Bot(command_prefix = "!", description = "Le meilleur bot", intents=intents)
