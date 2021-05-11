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


youtube_dl.utils.bug_reports_message = lambda: ''

'''le format des vidéos que le bot va récupérer sur internet'''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

musics = {}


class Video:
    '''classe qui va permettre au bot d'aller chercher la vidéo sur youtube'''
    def __init__(self, link):
        try :
            requests.get(link)
        except:
            video = ytdl.extract_info(f"ytsearch:{link}", download=False)["entries"][0]
            self.url = video["webpage_url"]
            self.stream_url = video["url"]
        else:
            video = ytdl.extract_info(link, download=False)
            self.url = video["webpage_url"]
            self.stream_url = video["url"]


class Role(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

        self.role_message_id = 829313507974840370 # ID du message auquel réagir afin d'ajouter/retirer un rôle
        self.emoji_to_role = {
            '😂': 824258848369541210, #ID du rôle associé à l'émoji
            '😄': 829095142010257479, 
               }  

    @commands.Cog.listener() 
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Donne un rôle selon l'émoji utilisé."""
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        try:
            print(payload.emoji.name)
            role_id = self.emoji_to_role[payload.emoji.name]
        except KeyError:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        await payload.member.add_roles(role)
   
    @commands.Cog.listener() 
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Retire le rôle en lien avec l'émoji."""
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            return

        try:
            await member.remove_roles(role)
        except:
            pass
