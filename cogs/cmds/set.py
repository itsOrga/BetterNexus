import discord
import requests
import PIL
import io
import json

from urllib.request import urlopen
from PIL import Image
from discord.ext import commands
from discord.commands import slash_command, Option
from playfunc import player_embed
from fongo import player_number, game_started, check_player, check_server, get_guild_infos
from errors import embed_error

class SetCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description = "Set a card on the board")

    async def set(self, ctx, where:
                 Option(
                     type = str, 
                     choices = ["A", "a", "B", "b", "C",
                               "c", "D", "d", "E", "e",
                               "t", "m", "n"],
                     
                     description = "Where are you setting the card ?",
                     required = True)
    ):

        if not check_server(ctx.guild):
            await ctx.respond(embed = embed_error("server_not_setup"))
            return()
        
        if not game_started(ctx.guild):
            await ctx.respond(embed = embed_error("game_not_started"))
            return()

        if not check_player(ctx.author, ctx.guild):
            await ctx.respond(embed = embed_error("not_in_game"))
            return()

        with open("board.json", "r") as f:
            board = json.load(f)

        player_num = player_number(ctx.author, ctx.guild)
        board_msg_id = get_guild_infos(ctx.guild)[1]
        board_channel_id = get_guild_infos(ctx.guild)[0]
        board_channel = await ctx.guild.fetch_channel(board_channel_id)
        board_msg = await board_channel.fetch_message(board_msg_id)

        print(player_num, ctx.author)
        position = board[str(player_num)][where]     

        board_im = Image.open(str(ctx.guild.id) + ".png")
        
        card = Image.open("set_card.png")
        card_resized = card.resize((240,240))

        card_copy = card_resized.copy()
        board_im.paste(card_copy, position)

        
        board_im.save(str(ctx.guild.id) + ".png")

        embed = player_embed(player_num)

        file = discord.File(str(ctx.guild.id) + ".png")
        embed.set_image(url="https://media.discordapp.net/attachments/1030522206750507092/1066418404573061240/temp.png?width=1440&height=393")

        await ctx.respond(f"You've set a card in your **{where}** zone !")
        await board_msg.edit(embed = embed, attachments = [], file = file)
        
def setup(bot):
    bot.add_cog(SetCard(bot))