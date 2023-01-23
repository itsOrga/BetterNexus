import discord
import os
from disuniter import keepAlive
import tracemalloc
bot = discord.Bot()

tracemalloc.start()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    game = discord.Game("with the API")
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.event
async def bot_activity():
    await bot.wait_until_ready()
    typ = discord.ActivityType.listening()
    activity = discord.Activity(type=typ)
    await bot.change_presence(activity=activity)

    
# Creating Slash Commands
    
for file in os.listdir("./cogs/cmds"):
    if file.endswith(".py"):
        bot.load_extension("cogs.cmds." + file[:-3])
		
for file in os.listdir("./cogs/evts"):
    if file.endswith(".py"):
        bot.load_extension("cogs.evts." + file[:-3])


bot.loop.create_task(bot_activity())
bot.run("MTAzMzA5NjExNDc1ODQ5NjMyNw.GXs7_Q.4C4CF3pWXvn8hjE347rM0voMIvmQPclhCGPNvQ")