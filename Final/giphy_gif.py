import discord
from discord.ext import commands
import random
import giphy_client
from giphy_client.rest import ApiException
from Bot_activ import bot


giphy_token = 'giphy API'

api_instance = giphy_client.DefaultApi()


async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(giphy_token, query, limit=50, rating='g')
        lst = list(response.data)
        gif = random.choices(lst)
        return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

@bot.command()
async def punch(ctx):
    gif = await search_gifs('anime punch')
    await ctx.send(gif)

@bot.command()
async def slap(ctx):
    gif = await search_gifs('anime slap')
    await ctx.send(gif)

@bot.command()
async def sleepy(ctx):
    gif = await search_gifs('anime sleepy')
    await ctx.send(gif)


@bot.command()
async def food(ctx):
    gif = await search_gifs('anime food')
    await ctx.send(gif)

