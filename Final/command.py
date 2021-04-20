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
import cowsay_modif
from Bot_activ import bot


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

@bot.command()
async def cow(ctx, *, texte):
    res = cowsay_modif.get_output_string('cow', texte)
    for line in res:
        await ctx.send(line)
