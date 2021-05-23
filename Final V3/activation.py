from Bot_activ import bot
import classe
import command
import event
import gif
import dessins
import morpion

bot.add_cog(classe.Role(bot))
bot.add_cog(command.Utilitaires(bot))
bot.add_cog(command.Fun(bot))
bot.add_cog(dessins.Dessins(bot))

bot.run("Token")
