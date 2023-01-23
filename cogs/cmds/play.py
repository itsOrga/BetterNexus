
import requests
import playfunc
import discord
import fongo
import PIL
import io
from fongo import check_server, game_started, check_player, start_game, end_game, get_guild_infos, player_number
from discord.commands import slash_command, Option
from urllib.request import urlopen
from discord.ext import commands
from errors import embed_error
from discord import Option
from PIL import Image
from playfunc import idle_embed

class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()

    async def play(self, ctx,
    player_2: Option(
        discord.Member, "Player 2 (you are player 1)"
    ),
    player_3: Option(
        discord.Member, "Player 3", required = True
    ),
    player_4: Option(
        discord.Member, "Player 4", required = False
    )):
    
        if not check_server(ctx.guild):
            await ctx.respond(embed = embed_error("server_not_setup"))
            return()
        
        if game_started(ctx.guild):
            await ctx.respond(embed = embed_error("already_started"))
            return()

        try:
            p4_id = player_4.id
        except:
            p4_id = None

        players_query = [
            {"id": ctx.author.id,
            "number": 1},
            {"id": player_2.id,
            "number": 2},
            {"id": player_3.id,
            "number": 3},
            {"id": p4_id,
            "number": 4}
        ]

        for player in players_query:
            if player["id"] is None:
                players_query.remove(player)

        start_game(players_query, ctx.guild)
        board_im = Image.open(f"{str(len(players_query))}p_board.png")
        board_im.save(str(ctx.guild.id) + ".png")
        await ctx.respond("Succes")
        

    @slash_command()

    async def end(self, ctx):
    
        if not check_server(ctx.guild):
            await ctx.respond(embed = embed_error("server_not_setup"))
            return()
        
        if not game_started(ctx.guild):
            await ctx.respond(embed = embed_error("game_not_started"))
            return()

        if not check_player(ctx.author, ctx.guild):
            await ctx.respond(embed = embed_error("not_in_game"))
            return()

        board_msg_id = get_guild_infos(ctx.guild)[1]
        board_channel_id = get_guild_infos(ctx.guild)[0]
        board_channel = await ctx.guild.fetch_channel(board_channel_id)
        board_msg = await board_channel.fetch_message(board_msg_id)

        embed = idle_embed()

        board_im = Image.open(f"4p_board.png")
        board_im.save(str(ctx.guild.id) + ".png")

        end_game(ctx.guild)
        await ctx.respond("Succesfully ended the game")

        file = discord.File(str(ctx.guild.id) + ".png")
        embed.set_image(url="https://media.discordapp.net/attachments/1030522206750507092/1066418404573061240/temp.png?width=1440&height=393")

        await board_msg.edit(embed = embed, attachments = [], file = file)

def setup(bot):
    bot.add_cog(PlayCommand(bot))
