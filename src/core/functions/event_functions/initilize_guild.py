import discord
import config

async def initilize_guild(guild: discord.Guild, bot):
    if not config.auto_init:
      return
    
    db = bot.mongoConnect[config.dbcollection]
    guild_collection = db["guild_data"]
    guild_id = str(guild.id)
    
    guild_data = await guild_collection.find_one({"_id": guild_id})
     
    if not guild_data:
       guild_data = {"_id": guild_id}       
       
    await guild_collection.update_one({"_id": guild_id}, {"$set": guild_data}, upsert=True)     


  #WDStudio PROPERTY owned by WDStudio
#© WDStudio 2024      