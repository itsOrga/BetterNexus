import discord
import requests
import PIL
import io

from urllib.request import urlopen
from PIL import Image
from discord.ext import commands
from discord.commands import slash_command, Option
from fongo import get_guild_infos, player_number, check_player, check_server, game_started
from playfunc import clear_embed
from errors import embed_error

class ClearBoardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()

    async def clear(self, ctx):

        if not check_server(ctx.guild):
            await ctx.respond(embed = embed_error("server_not_setup"))
            return()
        
        if not game_started(ctx.guild):
            await ctx.respond(embed = embed_error("game_not_started"))
            return()

        if not check_player(ctx.author, ctx.guild):
            await ctx.respond(embed = embed_error("not_in_game"))
            return()

        player_num = player_number(ctx.author, ctx.guild)
        board_msg_id = get_guild_infos(ctx.guild)[1]
        board_channel_id = get_guild_infos(ctx.guild)[0]
        board_channel = await ctx.guild.fetch_channel(board_channel_id)
        board_msg = await board_channel.fetch_message(board_msg_id)

        board_number = get_guild_infos(ctx.guild)[2]

        board_im = Image.open(f"{str(board_number)}p_board.png")
        board_im.save(str(ctx.guild.id) + ".png")

        embed = clear_embed(player_num)
        file = discord.File(str(ctx.guild.id) + ".png")

        await ctx.respond("The board was cleared !")
        await board_msg.edit(embed = embed, attachments = [], file = file)

def setup(bot):
    bot.add_cog(ClearBoardCommand(bot))