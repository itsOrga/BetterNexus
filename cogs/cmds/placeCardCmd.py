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

class PlaceCardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description = "Place a card on the board")

    async def place(self, ctx, method:
                       
                 Option(
                     type = str, 
                     description = "Parameter used to idetntify the card",
                     choices = ["by name", "by id"],
                     required = True), value:
                   
                 Option(
                     type = str, 
                     description = "The ID or name of the card",
                     required = True), where:

                 Option(
                     type = str, 
                     choices = ["A", "a", "B", "b", "C",
                               "c", "D", "d", "E", "e",
                               "t", "m", "n"],
                     
                     description = "Where are you placing the card ?",
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
        way = method[3:]

            
        parameters = {way: value}
                 
        response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php", params = parameters)

        jsn = response.json()
        data = jsn.get("data")[0]
        id = data.get("id")
        name = data.get("name")
        url = "https://images.ygoprodeck.com/images/cards_cropped/{}.jpg".format(id)
        
        board_im = Image.open(str(ctx.guild.id) + ".png")
        response2 = requests.get(url = url, headers = {"User-Agent": "Mozilla/5.0"})
        
        card = Image.open(io.BytesIO(response2.content))
        card_resized = card.resize((240,240))

        card_copy = card_resized.copy()
        board_im.paste(card_copy, position)

        
        board_im.save(str(ctx.guild.id) + ".png")

        embed = player_embed(player_num)

        file = discord.File(str(ctx.guild.id) + ".png")
        embed.set_image(url="https://media.discordapp.net/attachments/1030522206750507092/1066418404573061240/temp.png?width=1440&height=393")

        await ctx.respond(f"You've placed **{name}** in your **{where}** zone !")
        await board_msg.edit(embed = embed, attachments = [], file = file)
        
def setup(bot):
    bot.add_cog(PlaceCardCommand(bot))