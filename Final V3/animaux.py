import discord
from discord.ext import commands
import cowsay_modif
from Bot_activ import bot


class Dessins(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.command()
    async def cow(self, ctx, *, texte):
        "dessine une vache"
        res = cowsay_modif.get_output_string('cow', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')

    @commands.command()
    async def dragon(self, ctx, *, texte):
        "dessine un dragon"
        res = cowsay_modif.get_output_string('dragon', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def demon(self, ctx, *, texte):
        "dessine un démon"
        res = cowsay_modif.get_output_string('daemon', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def cheese(self, ctx, *, texte):
        "dessine un personnage ressemblant à un fromage"
        res = cowsay_modif.get_output_string('cheese', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')

    @commands.command()
    async def beavis(self, ctx, *, texte):
        "dessine un personnage de dessin animé américain nommé beavis"
        res = cowsay_modif.get_output_string('beavis', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def ghost(self, ctx, *, texte):
        "dessine le symbole de ghostbusters"
        res = cowsay_modif.get_output_string('ghostbusters', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def kitty(self, ctx, *, texte):
        "dessine un félin"
        res = cowsay_modif.get_output_string('kitty', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def meow(self, ctx, *, texte):
        "dessine un chat"
        res = cowsay_modif.get_output_string('meow', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def milk(self, ctx, *, texte):
        "dessine un personnage sous forme de brique de lait"
        res = cowsay_modif.get_output_string('milk', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')

    @commands.command()
    async def pig(self, ctx, *, texte):
        "dessine un cochon"
        res = cowsay_modif.get_output_string('pig', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def dino(self,ctx, *, texte):
        "dessine un dinosaure"
        res = cowsay_modif.get_output_string('stegosaurus', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def stimpy(self, ctx, *, texte):
        "dessine un personnage de dessin animé américain nommé stimpy"
        res = cowsay_modif.get_output_string('stimpy', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def trex(self, ctx, *, texte):
        "dessine un trex"
        res = cowsay_modif.get_output_string('trex', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def turkey(self, ctx, *, texte):
        "dessine une dinde"
        res = cowsay_modif.get_output_string('turkey', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')


    @commands.command()
    async def turtle(self, ctx, *, texte):
        "dessine une tortue"
        res = cowsay_modif.get_output_string('turtle', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')

    @commands.command()
    async def tux(self, ctx, *, texte):
        "dessine un pingouin"
        res = cowsay_modif.get_output_string('tux', texte)
        image = "\n".join(res)
        await ctx.send(f'``` {image} ```')
