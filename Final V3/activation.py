from Bot_activ import bot
import classe
import command
import event
import tenor_gif_simple
import giphy_gif
import animaux

bot.add_cog(classe.Role(bot))
bot.add_cog(command.Music(bot))
bot.add_cog(command.Utilitaires(bot))
bot.add_cog(command.Fun(bot))
bot.add_cog(animaux.Dessins(bot))

bot.run("Token")
