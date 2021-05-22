import discord
from discord.ext import commands
import youtube_dl
import asyncio
import ffmpeg
import requests
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


@bot.command()
async def stop(ctx):
    """permet d'arrêter la musique et de déconnecter le bot du salon vocal"""
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []

@bot.command()
async def resume(ctx):
    """permet de relancer la musique après l'avoir mise en pause"""
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()

@bot.command()
async def pause(ctx):
    """permet de mettre la musique en pause"""
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()

@bot.command()
async def skip(ctx):
    """permet de passer la musique et d'écouter la suivante"""
    client = ctx.guild.voice_client
    client.stop()

    
def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)

@bot.command()
async def play(ctx, *, url):
    """fonction permettant au bot de jouer de la musique"""
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
        await ctx.send(f"Prochaine musique : {video.url}")
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)

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
