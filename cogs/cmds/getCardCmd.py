import discord
import requests
from discord.ext import commands
from discord.commands import slash_command, Option


class GetCardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()

    async def card(self, ctx, way:
                 Option(
                     type = str, 
                     description = "How do you want to get the card ?",
                     choices = ["by name", "by id"],
                     required = True), value:
                   
                 Option(
                     type = str, 
                     description = "The ID or name of the card ?",
                     required = True)
                 ):

        way = way[3:]
            
        parameters = {way: value}
                 
        response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php", params = parameters)

        json = response.json()
        data = json.get("data")[0]
        id = data.get("id")
        url = "https://images.ygoprodeck.com/images/cards_cropped/{}.jpg".format(id)
                          
        await ctx.respond(url)

def setup(bot):
    bot.add_cog(GetCardCommand(bot))