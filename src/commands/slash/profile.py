from discord import app_commands
import discord
from .functions.createProfile import createProfile
from .views.profileMenu import ProfileMenu 
import config
from core.logger.logger import logger

@app_commands.command(name="profile", description="Setup or see your profile!")
async def profile(interaction: discord.Interaction):
    try:
      db = Bot.mongoConnect['Justalk']
      profile_collection = db["profiles"]    
      uid = str(interaction.user.id)
      profile = await profile_collection.find_one({"_id": uid})
      
      if not profile:
         await createProfile(Bot, interaction)
         return
     
      embed = discord.Embed(title="Profile", description=f"Hello **{interaction.user.name}**\n{config.replycont} Total chats: **{profile['total_chats']}**\n{config.replycont} Current languages: `{', '.join(profile['langs'])}`\n{config.reply} Current region: {profile['region']}", color=config.embedcolor)
      await interaction.response.send_message(embed=embed, view=ProfileMenu(Bot, interaction))
    except Exception as e:
        logger.error(e)
    
    
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.add_command(profile)            