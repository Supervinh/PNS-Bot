import discord
from discord.ext import commands
import requests
import json
import random
from Bot_activ import bot


APItenor = "tenor API"
lmt = 50

@bot.command()
async def autre(ctx):
    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime slap', APItenor, lmt))
    if r.status_code == 200:
        top_gifs = json.loads(r.content)
    else:
        top_gifs = None
    number =  random.randrange(0,9)
    gif = top_gifs['results'][number]['media'][0]['gif']['url']
    await ctx.send(gif)
