# Bot
Projet de création d'un bot Discord dans le cadre d'un semestre 0 à l'école Polytech Nice Sophia.

En réalité le bot n'est pas "créé", nous utilisons pour cela l'espace développeur proposé par Discord, nous nous contentons de coder les différentes fonctionnalités que ce dernier pourra effectuer. 

Les fonctions codées peuvent être séparées en 2 parties, celles qui se déclenchent automatiquement par des actions spécifiques et celles que l'on appelle avec certaines commandes.

## Fonctions évènements

### 1.	Event : on_ready
Son but est simplement de changer l’activité du Bot sur discord. Une fois activé le Bot « joue à Si vous avez besoin d’aide, tapez ’!help’ ». De plus, une fois le Bot prêt, le message "Ton bot est prêt" est affiché dans la console.

### 2.	Event : on_command_error
Le but de cet event va être d’envoyer un message d’erreur dans un chat si une commande n’existe pas, si elle a mal été appelée (par exemple s’il manque un argument), si un utilisateur n’a pas les droits sur une action ou si l’utilisateur ne possède pas le rôle permettant d’utiliser la commande.

### 3.	Event : on_member_join
A chaque nouvel utilisateur sur le serveur, le Bot renverra 'Salut NomUtilisateur, je te souhaite la bienvenue sur le serveur !' avec une image en privé au nouvel utilisateur.

### 4.	Event : on_member_update
Cette fonction notifie quand un membre agit sur son profil dans le serveur. Si un membre du serveur change son statut, son surnom ou son activité, un message correspondant sera envoyé sur un salon textuel prédéfini (il suffit de copier l’identifiant du salon et de le coller dans la variable channel de l’event).

### 5.	Event : on_user_update
Il agit de la même manière que le précédant mais cette fois pour son avatar, son pseudo ou son numéro d’identification (il faudra de la même façon copier l’identifiant du salon où l’on souhaite recevoir les messages).

### 6.	Event : on_message_delete
Cet événement notifie quand un message d’un channel est effacé en citant le message et le nom de l’utilisateur ayant envoyé le message (il faudra également spécifier le salon textuel où recevoir les messages).

### 7.	Event : on_message_edit
Cet event notifie quand le message d’un channel est modifié en affichant l’utilisateur qui a modifié son message, ainsi que le message avant et après modification (il faudra également spécifier un salon pour recevoir les messages).

Le seul soucis étant que, de la façon dont nous l'avons codé, le salon dans lequel le bot envoie les notifications doit être codé en dur.

## Commandes

### 1.	Morpion :
La première chose que nous avons fait est d’importer une bibliothèque appelée random.
Afin de commencer la partie, l’utilisateur doit utiliser la commande !morpion et se mentionner lui-même ainsi que l’autre membre du serveur avec qui il veut jouer. La partie se lance et désigne aléatoirement un des deux joueurs pour commencer. Le premier joueur doit ainsi utiliser la commande !place et choisir un chiffre entre 1 et 9 afin de jouer. Vient ensuite le tour du deuxième qui doit réitérer l’action, et ce jusqu’à que la grille soit remplie ou que l’un des 2 joueurs gagne. Le code a été fait de sorte qu’on ne puisse lancer d’autre partie tant que la première n’est pas terminée, et que chaque joueur soit obligé de respecter l’ordre des tours.

### 2.	Dessins :
Afin de réaliser les différentes fonctions de ce fichier dessins.py, nous sommes partis d’une bibliothèque nommée cowsay.py, que l’on a légèrement modifié afin de satisfaire nos exigences. Les différentes commandes de ce fichier permettent au bot d’envoyer un “dessin“ prédéfini avec un message fourni par l’utilisateur. Par exemple :

 
L’utilisateur a le choix entre différents dessins qu’il aura le loisir de voir en utilisant la commande !help, ou en regardant directement dans le code.

### 3.	Gifs :
Afin d’utiliser ces fonctions l’utilisateur devra installer les bibliothèques requests, random et giphy_client et obtenir une clé API tenor et giphy et les recopier dans les variables APItenor et giphy_token du fichier gif.py.
Les personnes sur le serveur discord auront la possibilité de choisir entre tenor et gif pour leur recherche de gif. Les utilisateurs auront simplement à taper la commande !tenor ou !giphy suivi des termes de recherche voulus, afin que le bot renvoie un gif correspondant à cette recherche.

### 4.	Utilitaires :
Dans cette catégorie de fonction se trouvent des commandes afin de gérer ou, du moins, obtenir des informations sur le serveur ou ses membres.

a)	InfoServeur :
Cette fonction permet simplement au bot d’envoyer le nom du serveur, le nombre de personnes présentes sur le serveur, si le serveur à une description (None sinon) ainsi que le nombre de salons textuels et vocaux.

b)	userinfo :

Cette fonction permet de connaître l’identifiant, le pseudonyme ainsi que l’avatar d’un utilisateur présent sur le serveur. Si jamais le bot ne trouve pas l’utilisateur (erreur dans le nom, ou utilisateur non présent sur le serveur), alors il renvoie un message d’erreur.

c)	delete :

Cette fonction permet à utilisateur qui possède la permission gestion des messages d’effacer le nombre de messages qu’il souhaite d’un salon textuel. Le bot envoie un message pour dire le nombre de messages effacés puis l’efface après 4 secondes.

d)	Create_channel :

Ces fonctions permettent de créer au choix un salon textuel ou vocal avec les commandes create_channel_t et create_channel_v avec la possibilité de spécifier un nom pour ces salons (si aucun nom n’est spécifié, alors le salon créé sera nommé “hasard“ par défaut). L’utilisateur utilisant cette commande devra cependant avoir un rôle avec le nom “admin“ pour pouvoir l’utiliser (le nom du rôle peut être changé à la ligne @commands.has_role).

e)	Kick, ban, unban:

Comme leurs noms l’indiquent, ces commandes permettent de kick, ban ou unban un utilisateur. Pour les utiliser, l’utilisateur devra respectivement avoir les permissions kick_members et ban_members.

f)	Mute :

Afin d’utiliser les commandes suivantes, l’utilisateur devra avoir un rôle avec le nom “admin“ (peut également être modifié comme précédemment). L’utilisateur doit commencer par créer un rôle Muted, pour se faire, il a le choix entre 2 fonctions : createMutedRole et getMutedRole. La seconde est préférable à la première car elle va d’abord chercher si un tel rôle existe déjà sur le serveur et si ce n’est pas le cas, elle fera appel à la première pour le créer, alors que la première créera le rôle même s’il existe déjà, ce qui provoquera des doublons. L’utilisateur peut ensuite utiliser les commandes mute et unmute (en pouvant, s’il le souhaite, indiquer une raison) sur un membre du serveur afin de lui ajouter ou retirer le rôle Muted.


### 5.	Fun :

a)	Mot spécifique :

L’utilisateur peut modifier la fonction NARUTO du fichier commands.py afin que le bot réponde à un mot spécifique de son choix, par un autre mot spécifique.

b)	Janken:

Afin d’utiliser cette fonction, l’utilisateur devra installer la bibliothèque random.
Cette fonction permet à un utilisateur de jouer à Pierre, Feuille, Ciseaux avec le bot. L’utilisateur doit utiliser la commande !Janken suivi de son choix (Pierre, Feuille ou Ciseaux), le bot enverra également son choix et donnera le résultat du match (victoire, égalité ou défaite).

c)	Secret :

Le bot envoie un message prédéfini (que l’utilisateur peut modifier dans la fonction secret du fichier commands.py) sous forme de spoiler qu’il efface après 4 secondes.

d)	Choose:

Afin d’utiliser cette fonction, l’utilisateur devra installer la bibliothèque random.
Cette fonction permet à un membre du serveur de demander au bot de faire un choix parmi une liste de réponses. Par exemple, si l’on écrit !choose 1 2 3, le bot enverra comme réponse 1, 2 ou 3.

e)	Say :

Le bot efface le message de l’utilisateur puis renvoie le même message, ce qui peut faire croire aux autres membres ne connaissant pas cette fonction que le bot a envoyé un message lui-même.

f)	Chinese :

Le bot prend en paramètre un texte donné par l’utilisateur, et le réécrit dans une police différente qui donne l’impression d’une écriture chinoise.

g)	Get_quote :

Le bot va chercher une citation aléatoirement sur internet (en anglais) puis l’envoie sur le serveur.

h)	Internet :

Le bot prend en paramètre ce que l’utilisateur veut chercher sur google, puis lui affiche le premier résultat trouvé.

i)	_8ball :

Le bot possède une liste de réponses prédéfinies afin de répondre aléatoirement à des questions posées par un membre du serveur.

j)	Meteo :

Afin d’utiliser cette fonction, l’utilisateur doit installer la bibliothèque requests.
Un membre du serveur choisit la ville, ainsi que le moment dont il veut connaitre la température, le taux d’humidité, la vitesse du vent et l’état du ciel, c’est-à-dire actuellement, à une certaine heure (jusqu’à 48h), ou de la journée (jusqu’à 1 semaine).

k)	Music :

Ces fonctions sont celles demandant le plus de bibliothèques à installer, qui sont youtube_dl, asyncio, ffmpeg et requests.
Les membres du serveur ont la possibilité d’écouter de la musique dans un salon vocal grâce au bot, par recherche grâce à une url, ou par recherche sur youtube de façon automatique. Plusieurs musiques peuvent être mises à la suite afin d’en faire une liste, et les membres ont la possibilité d’agir sur la musique, comme pour la mettre en pause, la reprendre, l’arrêter etc…

### Rôles :

Dans le fichier classe.py, l’utilisateur à la possibilité de désigner un message (grâce à son identifiant) ainsi que des émojis particuliers afin que les membres puissent réagir avec ces derniers et obtenir (ou retirer) des rôles associés à ces émojis (grâce à leurs identifiants également).
