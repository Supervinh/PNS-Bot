import random
import discord
from discord.ext import commands
from urllib import parse, request
import requests
import json
import re
from Bot_activ import bot


class Utilitaires(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command()
    async def InfoServeur(self, ctx):
        """donne les informations générales du serveur"""
        serveur = ctx.guild
        salons_textes = len(serveur.text_channels)
        salons_voc = len(serveur.voice_channels)
        description_serv = serveur.description
        nombre_membres = serveur.member_count
        nom_serveur = serveur.name
        message = f"Le serveur **{nom_serveur}** contient *{nombre_membres}* personnes. \nLa description du serveur est {description_serv}. \nCe serveur possède {salons_textes} salons textuels et {salons_voc} salons vocaux."
        await ctx.send(message)

    @commands.command()
    async def userinfo(self, ctx: commands.Context, user: discord.User):
        """permet d'avoir des informations sur un utilisateur"""
        user_id = user.id
        username = user.name
        avatar = user.avatar_url
        await ctx.send('Membre trouvé: {} -- {}\n{}'.format(user_id, username, avatar))


    @userinfo.error
    async def userinfo_error(self, ctx: commands.Context, error: commands.CommandError):
        """renvoie un message d'erreur si l'utilisateur est introuvable"""
        if isinstance(error, commands.BadArgument):
            return await ctx.send('Impossible de trouver cet utilisateur.')

    @commands.command(name="del")
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, number: int):
        """Efface le nombre de messages souhaité"""
        messages = await ctx.channel.history(limit=number + 1).flatten()
        for each_message in messages:
            await each_message.delete()


    @commands.command()
    @commands.has_role('admin')
    async def create_channel_t(self, ctx, channel_name='hasard'):
        """Avec un rôle 'admin', permet de créer un salon textuel"""
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)


    @commands.command()
    @commands.has_role('admin')
    async def create_channel_v(self, ctx, channel_name='hasard'):
        """Avec un rôle 'admin', permet de créer un salon vocal"""
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_voice_channel(channel_name)


    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user : discord.User, *reason):
        """permet de kick un utilisateur si l'on a les permissions pour"""
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason = reason)
        await ctx.send(f"{user} a été kick pour la raison suivante : {reason}.")


    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user : discord.User, *reason):
        """permet de ban un utilisateur si l'on a les permissions pour"""
        reason = " ".join(reason)
        await ctx.guild.ban(user, reason = reason)
        await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, user):
        """permet de unban un utilisateur si l'on a les permissions pour"""
        userName, userId = user.split("#")
        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
                if i.user.name == userName and i.user.discriminator == userId:
                        await ctx.guild.unban(i.user)
                        await ctx.send(f"{user} à été unban.")
                        return
        await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

    @commands.command()
    @commands.has_role('admin')
    async def createMutedRole(self, ctx):
        """permet de créer un rôle "Muted"""
        mutedRole = await ctx.guild.create_role(name = "Muted",
                                                permissions = discord.Permissions(
                                                    send_messages = False,
                                                    speak = False),
                                                reason = "Creation du role Muted pour mute des gens.")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mutedRole, send_messages = False, speak = False)
        await ctx.send("Un rôle 'Muted' a été créé")
        return mutedRole

    @commands.command()
    @commands.has_role('admin')
    async def getMutedRole(self, ctx):
        """permet de voir s'il existe un rôle "Muted", et en crée un si ce n'est pas le cas"""
        roles = ctx.guild.roles
        for role in roles:
            if role.name == "Muted":
                await ctx.send("il existe un rôle 'Muted'")
                return role
        
        return await self.createMutedRole(ctx)

    @commands.command()
    @commands.has_role('admin')
    async def mute(self, ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
        """permet de mute un utilisateur"""
        mutedRole = await self.getMutedRole(ctx)
        await member.add_roles(mutedRole, reason = reason)
        await ctx.send(f"{member.mention} a été mute !")

    @commands.command()
    @commands.has_role('admin')
    async def unmute(self, ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
        """permet d'unmute un utilisateur"""
        mutedRole = await self.getMutedRole(ctx)
        await member.remove_roles(mutedRole, reason = reason)
        await ctx.send(f"{member.mention} a été unmute !")



class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.command()
    async def NARUTO(self, ctx):
        """commande répondant un mot spécifique à un autre mot spécifique"""
        await ctx.send("SASUKE!!!")



    @commands.command()
    async def Janken(self, ctx,choix):
        """Jouer à Pierre, Feuille, Ciseaux contre le bot"""
        liste=["Pierre", "Feuille", "Ciseaux"]
        choix_bot=random.choice(liste)
        await ctx.send(choix_bot)
        if choix == 'Pierre':
            if choix_bot == "Feuille":
                await ctx.send("J'ai gagné")
            elif choix_bot == "Ciseaux":
                await ctx.send("J'ai perdu, bien joué. Une revanche ?")
            else:
                await ctx.send("Tss, égalité, encore")
        elif choix == 'Feuille':
            if choix_bot == "Pierre":
                await ctx.send("J'ai perdu, bien joué. Une revanche ?")
            elif choix_bot == "Ciseaux":
                await ctx.send("J'ai gagné")
            else:
                await ctx.send("Tss, égalité, encore")
        elif choix == 'Ciseaux':
            if choix_bot == "Pierre":
                await ctx.send("J'ai gagné")
            elif choix_bot == "Feuille":
                await ctx.send("J'ai perdu, bien joué. Une revanche ?")
            else:
                await ctx.send("Tss, égalité, encore")
        else:
            await ctx.send("Il faut choisir entre Pierre, Feuille ou Ciseaux")


    @commands.command()         
    async def secret(self, ctx):
        """Quel est ce "secret" dont tu parles?"""
        if ctx.invoked_subcommand is None:
            await ctx.send('||Shh! Les murs nous écoutent||', delete_after=4)


    @commands.command()
    async def choose(self, ctx, *choices: str):
        """Faire un choix facilement."""
        await ctx.send(random.choice(choices))

    @commands.command()
    async def say(self, ctx, *texte):
        """Fais répéter au bot un message"""
        message = await ctx.channel.history(limit = 1).flatten()
        await message[0].delete()
        await ctx.send(" ".join(texte))
        

    @commands.command()
    async def chinese(self, ctx, *texte):
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


    @commands.command()
    async def get_quote(self, ctx):
        """permet d'avoir une citation aléatoire venant d'un site internet"""
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        await ctx.send(quote)

    @commands.command()
    async def internet(self, ctx, *, search):
        """permet de montrer une recherche internet demandée par l'utilisateur"""
        query_string = parse.urlencode({'search_query': search})
        html_content = requests.get('https://www.google.com/search?q=' + query_string, cookies={'CONSENT': 'YES+'})
        search_results = re.findall(r'/url\?q=http.*?"', html_content.text)
        await ctx.send(search_results[0])

    @commands.command()
    async def _8ball(self, ctx, *, question):
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



    #Donne les coordonnées géographiques de la ville voulue pour pouvoir avoir les prévisions météo de cette même ville
    def coordonnees(city, long_or_lat):
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=c21a9f12441f8209ffb56153f5be52b2'.format(city)
        res = requests.get(url)
        data = res.json()
        if long_or_lat == "longitude":
            position = data['coord']['lon']
        elif long_or_lat == "latitude":
            position = data['coord']['lat']
        return position


    #Donne la météo d'une ville jusqu'à 1 semaine à l'avance
    @commands.command()
    async def meteo(self, ctx, city, moment, compteur_jour_heure):
        """commande pouvant donner la météo d'une ville jusqu'à 1 semaine à l'avance. Il suffit de choisir la ville souhaitée, puis le moment que l'on souhaite entre 'current', 'hourly', 'daily'.
Si l'on veut la météo actuelle, il suffit d'écrire '<ville> current' suivi d'un nombre quelconque.
Si l'on veut la météo dans 10h par exemple (possible jusqu'à 48h, il faut choisir un nombre entre 0 et 47 inclus), il suffit d'écrire '<ville> hourly 9'.
Si l'on veut la météo dans 2 jours par exemple(possible jusqu'à 7 jours à l'avance, il faut choisir un chiffre entre 0 et 7 inclus), il suffit d'écrire '<ville> daily 2'."""
        latitude = Fun.coordonnees(city, "latitude")
        longitude = Fun.coordonnees(city, "longitude")
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=&appid=c21a9f12441f8209ffb56153f5be52b2'.format(latitude,longitude)
        res = requests.get(url)
        data = res.json()
        if compteur_jour_heure == "now" or compteur_jour_heure == "today":
            compteur_jour_heure = 0

        #Cette condition donne la météo à l'instant où elle est demandée
        if moment == "current":
            temperature = "%.1f" % (float(data[moment]['temp']) - 273.15)       #data[moment]['temp'] donne la température en kelvin / converti en °C et donné avec 1 chiffre significatif 
            humidite = float(data[moment]['humidity'])      #humidité en %      
            wind = "%.1f" % (float(data[moment]['wind_speed']) * 3.6)       #float(data[moment]['wind_speed'] donne la vitesse du vent en m/s / converti en m/s
            description = data[moment]['weather'][0]['description']     
            message = f"Température: **{temperature}°C** \nTaux d'humidité: **{humidite}%** \nVitesse du vent:  **{wind} km/h** \nEtat du ciel: **{description}**"
            await ctx.send(message)      
        #Cette condition donne la météo par heure jusqu'à 48 heures à l'avance
        elif moment == "hourly":
            if -1 < int(compteur_jour_heure) < 48:
              temperature = "%.1f" % (float(data[moment][int(compteur_jour_heure)]['temp']) - 273.15)
              humidite = float(data[moment][int(compteur_jour_heure)]['humidity']) 
              wind = "%.1f" % (float(data[moment][int(compteur_jour_heure)]['wind_speed']) * 3.6)
              description = data[moment][int(compteur_jour_heure)]['weather'][0]['description']
              message = f"Température: **{temperature}°C** \nTaux d'humidite: **{humidité}%** \nVitesse du vent:  **{wind} km/h** \nEtat du ciel: **{description}**"
              await ctx.send(message)
            else:
              message = f"Erreur valeur.\nVeuillez donner une valeur correcte (entre 0 et 47)."
              await ctx.send(message)
        #Cette condition donne la météo par jour jusqu'à 7 jours à l'avance
        elif moment == "daily":
            if -1 < int(compteur_jour_heure) < 8:
              temperature_jour = "%.1f" % (float(data[moment][int(compteur_jour_heure)]['temp']['day']) - 273.15)
              temperature_nuit = "%.1f" % (float(data[moment][int(compteur_jour_heure)]['temp']['night']) - 273.15)
              humidite = float(data[moment][int(compteur_jour_heure)]['humidity']) 
              wind = "%.1f" % (float(data[moment][int(compteur_jour_heure)]['wind_speed']) * 3.6)
              description = data[moment][int(compteur_jour_heure)]['weather'][0]['description']
              message = f"Température dans la journée: **{temperature_jour}°C** \nTempérature dans la nuit: **{temperature_nuit}°C** \nTaux d'humidité: **{humidite}%** \nVitesse du vent:  **{wind} km/h** \nEtat du ciel: **{description}**"
              await ctx.send(message)
            else:
              message = f"Erreur valeur.\nVeuillez donner une valeur correcte (entre 0 et 7)."
              await ctx.send(message)
        else:
            message = f"Erreur message.\nVeuillez donner le moment correct (current, hourly ou daily)."
            await ctx.send(message)

