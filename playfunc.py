import discord

def idle_embed() -> discord.Embed:
    embed = discord.Embed(
        title = "Board Available",
        description = "",
        color = discord.Color.green()
    )
    embed.set_footer(text = "Use /play to start a new game")
    return embed

def clear_embed(player_num: int) -> discord.Embed:
    embed = discord.Embed(
        title = "Board was cleared",
        description = "",
        color = discord.Color.dark_gray()
    )
    embed.set_footer(text = f"Cleared by player {player_num}")
    return embed

def player_embed(player_num: int) -> discord.Embed:
    embed = discord.Embed(
        title = "Board Available",
        description = "",
        color = discord.Color.darker_grey()
    )
    embed.color = discord.Color.yellow()
    embed.color = discord.Color.red() if player_num == 1 else embed.color
    embed.color = discord.Color.green() if player_num == 2 else embed.color
    embed.color = discord.Color.blue() if player_num == 3 else embed.color
    
    embed.set_footer(text = f"Player {player_num} just played")

    return embed