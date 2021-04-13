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

'''import le fichier bot tout seul pour chaque fichier séparé'''

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

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True

bot = commands.Bot(command_prefix = commands.when_mentioned, description = "Le meilleur bot", intents=intents)


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
async def play(ctx, url):
    """fonction permettant au bot de jouer de la musique"""
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
	    await ctx.send("Oups vous ne pouvez utilisez cette commande.")

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
    

@bot.command()
async def NARUTO(ctx):
    """commande répondant un mot spécifique à un autre mot spécifique"""
    await ctx.send("SASUKE!!!")

@bot.command()
async def InfoServeur(ctx):
    """donne les informations générales du serveur"""
    serveur = ctx.guild
    salons_textes = len(serveur.text_channels)
    salons_voc = len(serveur.voice_channels)
    description_serv = serveur.description
    nombre_membres = serveur.member_count
    nom_serveur = serveur.name
    message = f"Le serveur **{nom_serveur}** contient *{nombre_membres}* personnes. \nLa description du serveur est {description_serv}. \nCe serveur possède {salons_textes} salons textuels et {salons_voc} salons vocaux."
    await ctx.send(message)

@bot.command()
async def Janken(ctx,choix):
    """Jouer à Pierre, Feuille, Ciseaux contre le bot"""
    liste=["Pierre", "Feuille", "Ciseaux"]
    bot=random.choice(liste)
    await ctx.send(bot)
    if choix == 'Pierre':
        if bot == "Feuille":
            await ctx.send("J'ai gagné")
        elif bot == "Ciseaux":
            await ctx.send("J'ai perdu, bien joué. Une revanche ?")
        else:
            await ctx.send("Tss, égalité, encore")
    elif choix == 'Feuille':
        if bot == "Pierre":
            await ctx.send("J'ai perdu, bien joué. Une revanche ?")
        elif bot == "Ciseaux":
            await ctx.send("J'ai gagné")
        else:
            await ctx.send("Tss, égalité, encore")
    elif choix == 'Ciseaux':
        if bot == "Pierre":
            await ctx.send("J'ai gagné")
        elif bot == "Feuille":
            await ctx.send("J'ai perdu, bien joué. Une revanche ?")
        else:
            await ctx.send("Tss, égalité, encore")
    else:
        await ctx.send("Il faut choisir entre Pierre, Feuille ou Ciseaux")


@bot.command()         
async def secret(ctx):
    """Quel est ce "secret" dont tu parles?"""
    if ctx.invoked_subcommand is None:
        await ctx.send('||Shh! Les murs nous écoutent||', delete_after=4)


@bot.command()
async def userinfo(ctx: commands.Context, user: discord.User):
    """permet d'avoir des informations sur un utilisateur"""
    user_id = user.id
    username = user.name
    avatar = user.avatar_url
    await ctx.send('Membre trouvé: {} -- {}\n{}'.format(user_id, username, avatar))


@userinfo.error
async def userinfo_error(ctx: commands.Context, error: commands.CommandError):
    """renvoie un message d'erreur si l'utilisateur est introuvable"""
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
    """Avec un rôle 'admin', permet de créer un salon textuel"""
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command()
@commands.has_role('admin')
async def create_channel_v(ctx, channel_name='hasard'):
    """Avec un rôle 'admin', permet de créer un salon vocal"""
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
    """Fais répéter au bot un message"""
    await ctx.send(" ".join(texte))
    

@bot.command()
async def chinese(ctx, *texte):
    """Donne une "traduction en chinois" d'un texte donné par l'utilisateur"""
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
    """permet de kick un utilisateur si l'on a les permissions pour"""
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} a été kick pour la raison suivante : {reason}.")


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *reason):
    """permet de ban un utilisateur si l'on a les permissions pour"""
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

@bot.command()
@commands.has_role('admin')
async def unban(ctx, user, *reason):
    """permet de unban un utilisateur si l'on a les permissions pour"""
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
	    if i.user.name == userName and i.user.discriminator == userId:
		    await ctx.guild.unban(i.user, reason = reason)
		    await ctx.send(f"{user} à été unban.")
		    return
    await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()
@commands.has_role('admin')
async def createMutedRole(ctx):
    """permet de créer un rôle "Muted"""
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

@bot.command()
@commands.has_role('admin')
async def getMutedRole(ctx):
    """permet de voir s'il existe un rôle "Muted", et en crée un si ce n'est pas le cas"""
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
@commands.has_role('admin')
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    """permet de mute un utilisateur"""
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

@bot.command()
@commands.has_role('admin')
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    """permet d'unmute un utilisateur"""
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")


@bot.command()
async def get_quote(ctx):
    """permet d'avoir une citation aléatoire venant d'un site internet"""
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    await ctx.send(quote)

@bot.command()
async def internet(ctx, *, search):
    """permet de montrer une recherche internet demandée par l'utilisateur"""
    query_string = parse.urlencode({'search_query': search})
    html_content = requests.get('https://www.google.com/search?q=' + query_string, cookies={'CONSENT': 'YES+'})
    search_results = re.findall(r'/url\?q=http.*?"', html_content.text)
    await ctx.send(search_results[0])

@bot.command()
async def _8ball(ctx, *, question):
    """permet au bot de répondre à l'utilisateur"""
    reponses = ['Evidemment',
                "Je suis d'accord",
                "Ma réponse est non",
                "Je ne suis pas d'accord",
                "Pourquoi pas ?",
                "Je n'ai aucun doute dessus",
                "Oui",
                "Je n'ai pas bien compris la question, peux-tu répéter ?",
                "Mes sources me disent que non"]
    await ctx.send(f"Question : {question}\nAnswer : {random.choice(reponses)}")


bot.add_cog(Role(bot))

bot.run("token")
