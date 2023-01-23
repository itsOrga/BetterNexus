import discord

def embed_error(code:str) -> discord.Embed:
    
    message = "unknown"
    message = "this server is already in the database" if code == 'server_already_setup' else message
    message = "this server is not in the database yet, use </start:1064173824771366915> to set it up" if code == 'server_not_setup' else message
    message = "a game already started" if code == 'already_started' else message
    message = "this is not your turn" if code == 'not_your_turn' else message
    message = "you're not allowed to do this" if code == 'not_allowed' else message
    message = "you need to be in a game to do this" if code == 'not_in_game' else message
    message = "no game have started yet" if code == 'game_not_started' else message

    embeded_error = discord.Embed(
        title = "Error",
        description = message,
        color = discord.Color.red()
    )

    return embeded_error

def log_error(error) -> None:
    ...