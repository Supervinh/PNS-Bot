import random
import discord
from discord.ext import commands
import youtube_dl
import asyncio
import ffmpeg
from urllib import parse, request
import requests
import json
import re
from Bot_activ import bot

@bot.event
async def on_command_error(ctx, error):
    """Envoie un message si l'utilisateur se trompe dans les commandes"""
    if isinstance(error, commands.CommandNotFound):
	    await ctx.send("J'ai bien l'impression que cette commande n'existe pas :/")
    if isinstance(error, commands.MissingRequiredArgument):
	    await ctx.send("Il manque un argument.")
    elif isinstance(error, commands.MissingPermissions):
	    await ctx.send("Vous n'avez pas les permissions pour faire cette commande.")
    elif isinstance(error, commands.CheckFailure):
	    await ctx.send("Oups vous ne pouvez iutilisez cette commande.")

@bot.event
async def on_ready():
    print("Ton bot est prêt")

@bot.event
async def on_member_join(member):
    """Notifie quand quelqu'un arrive sur le serveur"""
    await member.create_dm()
    await member.dm_channel.send(f'Salut {member.name}, je te souhaite la bienvenue sur le serveur !')
    await member.dm_channel.send("https://i.pinimg.com/originals/31/e6/92/31e692bb314ef309603f83c4be7c803b.jpg")

@bot.event
async def on_member_update(before,after):
    """Notifie quand un membre agit sur son profil dans le serveur"""
    channel = bot.get_channel(820761843508838417)
    if before.status != after.status:
        message = f"L'utilisateur **{before}** a changé son statut de {before.status} en {after.status}"
        await channel.send(message) 
    if before.nick != after.nick:
        message = f"L'utilisateur **{before}** a changé son surnom de {before.nick} en {after.nick}"
        await channel.send(message)
    if before.activity != after.activity:
        message = f"L'utilisateur **{before}** est passé de l'activité {before.activity} à l'activité {after.activity}"
        await channel.send(message)


@bot.event
async def on_user_update(before,after):
    """Notifie quand un membre agit sur son profil"""
    channel = bot.get_channel (820761843508838417)
    if before.avatar != after.avatar:
        message = f"L'utilisateur **{before}** a changé son avatar de {before.avatar} en {after.avatar}"
        await channel.send(message) 
    if before.username != after.username:
        message = f"L'utilisateur **{before}** a changé son pseudo de {before.username} en {after.username}"
        await channel.send(message)
    if before.discriminator != after.discriminator:
        message = f"L'utilisateur **{before}** a changé son # de {before.discriminator} en {after.discriminator}"
        await channel.send(message)


@bot.event
async def on_message_delete(message):
    """Notifie quand un message est effacé"""
    channel = bot.get_channel (820761843508838417)
    await channel.send(f"Le message de {message.author} a été supprimé \n> {message.content}")

@bot.event
async def on_message_edit(before, after):
    """Notifie quand un message est modifié"""
    channel = bot.get_channel (820761843508838417)
    await channel.send(f"{before.author} a édité son message :\nAvant -> {before.content}\nAprès -> {after.content}")
    
