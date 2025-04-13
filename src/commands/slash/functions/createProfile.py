import discord
import config
from ..views.langSelect import langSelect


async def createProfile(bot, interaction: discord.Interaction):
    inDMS = False
    inDMS = False if interaction.guild is None else True
    uid = str(interaction.user.id)
    profile = {
        "_id": uid,
        "chat": {
            "waiting": False,
            "w_pers": False, # ? waiting for personalized chat
            "chatting": False,
            "partner": None
        },
        "total_chats": 0,
        "invisible": False,
    }
    
    eStr = "*(it's recommended to do this setup in the bot's DMS)*"
    if inDMS == False:
        eStr = ""
        
    embed = discord.Embed(title="New profile", description=f"Hello **{interaction.user.name}**, Welcome to Justalk! This is the profile setup.\nPlease pick the language(s) you know, click your first languages first.\n{eStr}", color=config.embedcolor)
    await interaction.response.send_message(embed=embed, view=langSelect(profile, bot, interaction, True))
  #  await profile_collection.update_one({"_id": str(uid)}, {"$set": profile}, upsert=True)     