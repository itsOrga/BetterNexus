import pymongo
import discord
import os


#password = os.environ["MONGO_PASS"]
password = "vWa9jbKvkPSuhkLa"
client = pymongo.MongoClient(f"mongodb+srv://nexus:{password}@cluster0.omtbfnu.mongodb.net/?retryWrites=true&w=majority")
db = client.test

manager = client["manager"]
users_col = manager["users"]
servers_col = manager["servers"]

# Functions
# Check if its a member's first connection

def check_server(guild:discord.Guild):
    filter = {"server": guild.id}
    if servers_col.find_one(filter) is None:
        return False
    else:
        return True

def setup_server(guild:discord.Guild, board_msg:discord.Message):
    query = {"server": guild.id,
    "board_channel": board_msg.channel.id,
    "board_message": board_msg.id,
    "game_has_started": False,
    "current_players": [{}]}

    servers_col.insert_one(query)

def game_started(guild:discord.Guild):
    filter = {"server": guild.id}
	
    target = servers_col.find_one(filter)
    has_started = target["game_has_started"]
    
    return True if (has_started) else False


def check_player(member:discord.Member, guild:discord.Guild):
    filter = {"server": guild.id}
	
    document = servers_col.find_one(filter)
    target = None

    for player in document["current_players"]:
        if player["id"] == member.id:
            return True

    if target is None : return False

def player_number(member:discord.Member, guild:discord.Guild):
    filter = {"server": guild.id}
	
    document = servers_col.find_one(filter)
    target = None

    for player in document["current_players"]:
        if player["id"] == member.id:
            target = player

    number = target["number"]

    return number

def start_game(players_query: list, guild: discord.Guild):

    try:
        server_doc = servers_col.find_one({"server": guild.id})
        
        servers_col.find_one_and_update({"server": guild.id},
        {"$set" :
        {"current_players" : players_query, "game_has_started" : True}})
		
        return True

    except Exception as e:
        print(e, guild.id)
        return False

def end_game(guild: discord.Guild):

    try:
        server_doc = servers_col.find_one({"server": guild.id})
        
        servers_col.find_one_and_update({"server": guild.id},
        {"$set" :
        {"current_players" : [], "game_has_started" : False}})
		
        return True

    except Exception as e:
        print(e, guild.id)
        return False

def get_guild_infos(guild: discord.Guild):

    try:
        server_doc = servers_col.find_one({"server": guild.id})
        board_channel = server_doc["board_channel"]
        board_message = server_doc["board_message"]
        players = server_doc["current_players"]
        return board_channel, board_message, len(players)

    except Exception as e:
        print(e)
        return False, e

def get_stock(category_id:str):

    try:
        category_data = users_col.find_one({"category_id":category_id})
        stock_list = category_data["stock"]
        return stock_list, len(stock_list)

    except Exception as e:
        print(e)
        return False, e
        
def get_free_stock(category_id:str):

    try:
        category_data = users_col.find_one({"category_id":category_id})
        stock_list = category_data["stock"]
        return stock_list, len(stock_list)

    except Exception as e:
        print(e)
        return False, e


def generate_acc(category_id:str, amount, col = "premium"):

    collection = users_col if col == "premium" else users_col

    document = collection.find_one({"category_id" : category_id})
    if document is None:
        return 3
    stock = document["stock"]

    if len(stock) <=0:
        return 1 
    if len(stock) < amount:       
        return 4

    
    accounts = stock[0:amount]
        
    collection.update_one(
        { "category_id": category_id},
        { "$pull": { "stock": {"$in": accounts} }}) 
    
    return accounts

def test_mongo(category_id:str, amount = 1):

    cursor = users_col.find()
    return cursor

def add_stock(category_id, stock_list:str, col = "premium"):
    collection = users_col if col == "premium" else users_col
    try:
        collection.update_one(
        {'category_id': category_id},
        { '$addToSet': { 'stock': { '$each': stock_list } } })
        return True
    except:
        return False

def restock_keys(category_id, keys):
    try:
        users_col.update_one(
        {'category_id': category_id},
        { '$addToSet': { 'stock': { '$each': keys } } })
        return True
    except:
        return False


def create_category(category_id):
				  
    try:
        if (users_col.find_one({"category_id" : category_id})) is not None:
            return False
            
        query = {"category_id": category_id,
                "stock": []}
        users_col.insert_one(query)
        return True

    except Exception as e:
        return False, e

def get_categories_ids(col = "premium"):
    collection = users_col if col == "premium" else users_col
    categories = []
    cursor = collection.find()
    for document in cursor:
        categories.append(document["category_id"])
        
    return categories

def redeem_key(member:discord.Member, keys):

    target = users_col.find_one(
        {"stock" : {"$in" : keys}}
    )
    if target is None:
        return 1
        
    key_stock = target["stock"]
    bool = (all([key in key_stock for key in keys]))
    if not bool:
        return 1
    

    found = users_col.find_one_and_update(
        {"stock" : {"$in" : keys}},
        {"$pull" : {"stock" : {"$in" : keys}}}
    )
    value = found["value"]
    category = found["category_id"]
    add_cleanies(member, len(keys)*value)
    return value, category

def get_price(category_id, col = "premium"):
    collection = users_col if col == "premium" else users_col

    document = collection.find_one(
        {"category_id": category_id}
    )
    price = document["price"]
    return price
    
        
