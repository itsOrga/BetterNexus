
import requests
import playfunc
import discord
import fongo
import PIL
import io
from discord.commands import slash_command, Option
from fongo import check_server, setup_server
from urllib.request import urlopen
from discord.ext import commands
from errors import embed_error
from discord import Option
from PIL import Image
from playfunc import idle_embed

class SetupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()

    async def start(self, ctx):
        if check_server(ctx.guild):
            await ctx.respond(embed = embed_error("server_already_setup"))
            return()
        else:
            channel = await ctx.guild.create_text_channel(name = "board-channel",
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
            })

            embed = idle_embed()
            print(embed.title)

            file = discord.File("4p_board.png")
            embed.set_image(url="https://media.discordapp.net/attachments/1030522206750507092/1066418404573061240/temp.png?width=1440&height=393")

            board_msg = await channel.send(embed = embed, file = file)

            setup_server(ctx.guild, board_msg)

            
            thread = await board_msg.create_thread(name = "Game Room")
            rules = await thread.send("Dueling Nexus is a free to play Yu-Gi-Oh! Online game. Dueling Nexus is automated, making it the perfect online platform for testing cards and learning the game as its impossible to make an invalid move, this also makes it impossible for your opponents to cheat.\nDueling Nexus works on all major operating systems including Windows, Mac, Linux, Android, iOS, Chrome OS and others. Due to its low power requirements, nearly any device is capable of playing on Dueling Nexus at good speeds.\nDueling Nexus is frequently updated, new cards are added shortly after being announced, long before they are printed and released to the general public. This gives our players an unique opportunity to test new cards before they decide to purchase them.\nNexus AI is an advanced dueling robot players can use to test their decks. Nexus AI can use over 30 unique decks. To duel the AI start by making a deck in our Deck Editor and then head over to the Duel Zone and click on: Play against a basic bot. ")
            await rules.pin(reason="Rules of the game")

            await ctx.respond(f"Succes! You can start using the commands in the {thread.mention} created in {channel.mention}")
            

def setup(bot):
    bot.add_cog(SetupCommand(bot))
