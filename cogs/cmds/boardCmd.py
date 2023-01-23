import discord
import requests
import PIL
import io

from urllib.request import urlopen
from PIL import Image
from discord.ext import commands
from discord.commands import slash_command, Option

class BoardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@slash_command()

    async def board(self, ctx):
            
        await ctx.respond("Success !", file = discord.File(str(ctx.guild.id) + ".png"))

def setup(bot):
    bot.add_cog(BoardCommand(bot))