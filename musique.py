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
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]


intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True

bot = commands.Bot(command_prefix = commands.when_mentioned, description = "Le meilleur bot", intents=intents)


@bot.command()
async def stop(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def skip(ctx):
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
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)

'''
async def ensure_voice(self, ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()
'''

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
    channel = bot.get_channel(820761843508838417)
    if before.status != after.status:
        message = f"L'utilisateur **{before}** a changé son statut de {before.status} en {after.status}"
        await channel.send(message) 
    if before.nickname != after.nickname:
        message = f"L'utilisateur **{before}** a changé son surnom de {before.nickname} en {after.nickname}"
        await channel.send(message)
    if before.activity != after.activity:
        message = f"L'utilisateur **{before}** est passé de l'activité {before.activity} à l'activité {after.activity}"
        await channel.send(message)


@bot.event
async def on_user_update(before,after):
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
    channel = bot.get_channel (820761843508838417)
    await channel.send(f"Le message de {message.author} a été supprimé \n> {message.content}")

@bot.event
async def on_message_edit(before, after):
    channel = bot.get_channel (820761843508838417)
    await channel.send(f"{before.author} a édité son message :\nAvant -> {before.content}\nAprès -> {after.content}")
    

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
@commands.has_permissions(manage_messages=True)
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

@bot.command()
async def say(ctx, *texte):
    await ctx.send(" ".join(texte))

@bot.command()
async def chinese(ctx, *texte):
	chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
	chineseText = []
	for word in texte:
		for char in word:
			if char.isalpha():
				index = ord(char) - ord("a")
				transformed = chineseChar[index]
				chineseText.append(transformed)
			else:
				chineseText.append(char)
		chineseText.append(" ")
	await ctx.send("".join(chineseText))

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} a été kick.")


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

@bot.command()
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")


async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

@bot.command()
async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")




bot.run("token")


