from random import *
import discord
from discord.ext import commands
import youtube_dl
import asyncio
import ffmpeg

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
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

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()




intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True

bot = commands.Bot(command_prefix = commands.when_mentioned, description = "Le meilleur bot", intents=intents)

bot.add_cog(Music(bot))

@bot.event
async def on_ready():
    print("Ton bot est prêt")

@bot.event
async def on_member_join(member):
    """Notifie quand quelqu'un arrive sur le serveur"""
    await member.create_dm()
    await member.dm_channel.send(f'Salut {member.name}, je te souhaite la bienvenue sur le serveur !')
    await member.dm_channel.send("https://i.pinimg.com/originals/31/e6/92/31e692bb314ef309603f83c4be7c803b.jpg")

'''@bot.event
async def on_member_update(before,after):
    channel = bot.get_channel(820761843508838417)
    await channel.send(before)
    await channel.send(after)'''
#before.status, nickname etc...

    
@bot.event
async def on_message(message):
    if message.author != bot.user:
        if "dis" in message.content.lower():
            await message.channel.send(message.content.lower())
    await bot.process_commands(message)

@bot.command()
async def NARUTO(ctx):
    await ctx.send("SASUKE!!!")

@bot.command()
async def InfoServeur(ctx):
    serveur = ctx.guild
    salons_textes = len(serveur.text_channels)
    salons_voc = len(serveur.voice_channels)
    description_serv = serveur.description
    nombre_membres = serveur.member_count
    nom_serveur = serveur.name
    message = f"Le serveur **{nom_serveur}** contient *{nombre_membres}* personnes. \nLa description du serveur est {description_serv}. \nCe serveur possède {salons_textes} salons textuels et {salons_voc} salons vocaux."
    await ctx.send(message)

'''@bot.command()
async def Janken(ctx):
    await ctx.send("Pierre, Feuille ou Ciseaux")
    liste=["Pierre", "Feuille", "Ciseaux"]
    bot=choice(liste)
    @bot.command()
    async def Pierre(ctx):
        if bot == "Feuille":
            await ctx.send("J'ai gagné")
        elif bot == "Ciseaux":
            await ctx.send("J'ai perdu, bien joué. Une revanche ?")
        else:
            await ctx.send("Tss, égalité, encore")
    @bot.command()
    async def Feuille(ctx):
        if bot == "Pierre":
            await ctx.send("J'ai perdu, bien joué. Une revanche ?")
        elif bot == "Ciseaux":
            await ctx.send("J'ai gagné")
        else:
            await ctx.send("Tss, égalité, encore")
    @bot.command()
    async def Ciseaux(ctx):
        if bot == "Pierre":
            await ctx.send("J'ai gagné")
        elif bot == "Feuille":
            await ctx.send("J'ai perdu, bien joué. Une revanche ?")
        else:
            await ctx.send("Tss, égalité, encore") '''

@bot.command()
async def Pierre(ctx):
    liste=["Pierre", "Feuille", "Ciseaux"]
    bot=choice(liste)
    await ctx.send(bot)
    if bot == "Feuille":
        await ctx.send("J'ai gagné")
    elif bot == "Ciseaux":
        await ctx.send("J'ai perdu, bien joué. Une revanche ?")
    else:
        await ctx.send("Tss, égalité, encore")
@bot.command()
async def Feuille(ctx):
    liste=["Pierre", "Feuille", "Ciseaux"]
    bot=choice(liste)
    await ctx.send(bot)
    if bot == "Pierre":
        await ctx.send("J'ai perdu, bien joué. Une revanche ?")
    elif bot == "Ciseaux":
        await ctx.send("J'ai gagné")
    else:
        await ctx.send("Tss, égalité, encore")
@bot.command()
async def Ciseaux(ctx):
    liste=["Pierre", "Feuille", "Ciseaux"]
    bot=choice(liste)
    await ctx.send(bot)
    if bot == "Pierre":
        await ctx.send("J'ai gagné")
    elif bot == "Feuille":
        await ctx.send("J'ai perdu, bien joué. Une revanche ?")
    else:
        await ctx.send("Tss, égalité, encore")

@bot.command()         
async def secret(ctx):
    """What is this "secret" you speak of?"""
    if ctx.invoked_subcommand is None:
        await ctx.send('||Shh! Les murs nous écoutent||', delete_after=4)


@bot.command()
async def userinfo(ctx: commands.Context, user: discord.User):
    user_id = user.id
    username = user.name
    avatar = user.avatar_url
    await ctx.send('Membre trouvé: {} -- {}\n{}'.format(user_id, username, avatar))


@userinfo.error
async def userinfo_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.BadArgument):
        return await ctx.send('Impossible de trouver cet utilisateur.')

@bot.command(name="del")
async def delete(ctx, number: int):
    """Efface le nombre de messages souhaité"""
    messages = await ctx.channel.history(limit=number + 1).flatten()
    for each_message in messages:
        await each_message.delete()


@bot.command()
@commands.has_role('admin')
async def create_channel_t(ctx, channel_name='hasard'):
    """commencer par créer un rôle 'admin'"""
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command()
@commands.has_role('admin')
async def create_channel_v(ctx, channel_name='hasard'):
    """commencer par créer un rôle 'admin'"""
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_voice_channel(channel_name)


@bot.command()
async def choose(ctx, *choices: str):
    """Faire un choix facilement."""
    await ctx.send(random.choice(choices))







bot.run("token")


