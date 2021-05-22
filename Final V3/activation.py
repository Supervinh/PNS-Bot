from Bot_activ import bot
import classe
import command
import event
import gif
import animaux
import morpion

bot.add_cog(classe.Role(bot))
bot.add_cog(command.Utilitaires(bot))
bot.add_cog(command.Fun(bot))
bot.add_cog(animaux.Dessins(bot))

bot.run("Token")
