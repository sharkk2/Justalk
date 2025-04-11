from discord import app_commands
import discord
import config
from core.logger.logger import logger

@app_commands.command(name="disconnect", description="Disconnect from a chat/waiting lobby")
async def command(interaction: discord.Interaction):
    try:
      await interaction.response.defer(thinking=True)  
        
      db = Bot.mongoConnect['Justalk']
      profile_collection = db["profiles"]    
      uid = str(interaction.user.id)
      profile = await profile_collection.find_one({"_id": uid})
      
      if not profile:
         embed = discord.Embed(description=f"{config.no} | Please make a profile first by doing `/profile`", color=config.embederrorcolor)
         await interaction.followup.send(embed=embed)
         return
     
     
      if not profile['chat']['chatting']:
        if profile['chat']['waiting']:
            profile['chat']["waiting"] = False
            profile['chat']['w_pers'] = False
            
            await profile_collection.update_one({"_id": uid}, {"$set": profile}, upsert=True)        
            embed = discord.Embed(description=f"You have been disconnected", color=config.embederrorcolor)
            await interaction.followup.send(embed=embed)  
            return
            
        else:
          embed = discord.Embed(description=f"{config.no} | You're already disconnected from any chat or waiting lobby", color=config.embederrorcolor)
          await interaction.followup.send(embed=embed, ephemeral=True)
          return
      
      profile['chat']["waiting"] = False
      profile['chat']['w_pers'] = False
      profile['chat']['chatting'] = False
      partner = profile['chat']['partner']
      if partner:
          chatter = await Bot.fetch_user(int(partner))
          if chatter:
              partner_profile = await profile_collection.find_one({"_id": partner})
              if partner_profile:
                  partner_profile['chat']['waiting'] = False
                  partner_profile['chat']['w_pers'] = False
                  partner_profile['chat']['chatting'] = False
                  partner_profile['chat']['partner'] = None
                  await profile_collection.update_one({"_id": partner}, {"$set": partner_profile}, upsert=True)
                  embed = discord.Embed(description=f"**{interaction.user.name}** has disconnected", color=config.embederrorcolor)
                  await chatter.send(embed=embed)
          profile['chat']['partner'] = None
      await profile_collection.update_one({"_id": uid}, {"$set": profile}, upsert=True)        
      embed = discord.Embed(description=f"You have been disconnected", color=config.embederrorcolor)
      await interaction.followup.send(embed=embed)  
          
        
     
     
    except Exception as e:
        logger.error(e)
    
    
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.add_command(command)            