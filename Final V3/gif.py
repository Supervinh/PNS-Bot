import discord
from discord.ext import commands
import requests
import json
import random
import giphy_client
from giphy_client.rest import ApiException
from Bot_activ import bot


APItenor = "API"
lmt = 50

giphy_token = 'TOKEN'

api_instance = giphy_client.DefaultApi()


@bot.command()
async def tenor(ctx, *, arg):
    """permet de chercher un gif sur la plateforme tenor"""
    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('{arg}', APItenor, lmt))
    if r.status_code == 200:
        top_gifs = json.loads(r.content)
    else:
        top_gifs = None
    number =  random.randrange(0,9)
    gif = top_gifs['results'][number]['media'][0]['gif']['url']
    await ctx.send(gif)


async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(giphy_token, query, limit=50, rating='g')
        lst = list(response.data)
        gif = random.choices(lst)
        return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

@bot.command()
async def giphy(ctx, *, arg):
    """permet de chercher un gif sur la plateforme giphy"""
    gif = await search_gifs(f'{arg}')
    await ctx.send(gif)

