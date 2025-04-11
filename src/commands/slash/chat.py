from discord import app_commands
import discord
from .functions.timeCalc import get_time
import config
from core.logger.logger import logger
import random
import time

@app_commands.command(name="chat", description="Go on a chat")
async def command(interaction: discord.Interaction, personalized: bool = False):
    try:   
      if interaction.guild:
         embed = discord.Embed(description=f"{config.no} | This command can only be used in the bot's DMs", color=config.embederrorcolor)
         await interaction.response.send_message(embed=embed, ephemeral=True)
         return
      
      await interaction.response.defer(thinking=True)  
        
      db = Bot.mongoConnect['Justalk']
      profile_collection = db["profiles"]    
      uid = str(interaction.user.id)
      profile = await profile_collection.find_one({"_id": uid})
      
      if not profile:
         embed = discord.Embed(description=f"{config.no} | Please make a profile first by doing `/profile`", color=config.embederrorcolor)
         await interaction.followup.send(embed=embed)
         return
     
      if profile['chat']['waiting'] or profile['chat']['w_pers']:
        embed = discord.Embed(description=f"{config.no} | You're already waiting, do `/disconnect` to leave", color=config.embederrorcolor)
        await interaction.followup.send(embed=embed)
        return
        
      if profile['chat']['chatting']:
        embed = discord.Embed(description=f"{config.no} | You're already in chat, do `/disconnect` to leave", color=config.embederrorcolor)
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
          
     
      profile['chat']["waiting"] = True 
      
      profile['chat']['w_pers'] = personalized 
      await profile_collection.update_one({"_id": uid}, {"$set": profile}, upsert=True)
      
      embed = discord.Embed(title="Chat", description=f"You're now waiting for a chat partner! Please wait a bit, it may take a while.", color=config.embedcolor)
      embed.set_footer(text="You can cancel the waiting by doing /disconnect")
      await interaction.followup.send(embed=embed)
      # partner matchmaking
      
      match = None
      attempts = 0
      while True:  
        my_status = await profile_collection.find_one({"_id": uid})
        if not my_status['chat'].get('waiting', True):  
          break  
          
        matches = []
        async for pro in profile_collection.find({"chat.waiting": True}):
            if pro['_id'] == uid:
                continue
            score = 0
            if personalized:
              user_langs = profile.get('langs', [])
              pro_langs = pro.get('langs', [])
          
              if user_langs and pro_langs:
                  if user_langs[0] == pro_langs[0]:
                      score += 2  
                  elif set(user_langs) & set(pro_langs):
                      score += 1  
          
              if pro.get('region') == profile.get('region'):
                  score += 1
          
              if score > 0:
                  matches.append((score, pro))
            else:
              if not pro['chat']['w_pers']:
                matches.append((1, pro))      


        if matches:
          my_status = await profile_collection.find_one({"_id": uid})
          if not my_status['chat'].get('waiting', True):  
            break  
          
          max_score = max(score for score, _ in matches)
          best_matches = [pro for score, pro in matches if score == max_score]  
          match = random.choice(best_matches)
          
          locked = profile_collection.find_one_and_update(
              {"_id": match['_id'], "chat.waiting": True, "chat.partner": None},
              {"$set": {"chat.waiting": False, "chat.partner": uid, "chat.chatting": True, "chat.w_pers": False}, "$inc": {"total_chats": 1}}
          )  
          
          if locked:
            my_status = await profile_collection.find_one({"_id": uid})
            if not my_status['chat'].get('waiting', True):  
              break  
            profile['chat']['waiting'] = False
            profile['chat']['partner'] = match['_id']
            profile['chat']['chatting'] = True 
            profile['chat']['w_pers'] = False
            profile['total_chats'] += 1
            await profile_collection.update_one({"_id": uid}, {"$set": profile}, upsert=True)
            
            pair = await Bot.fetch_user(match['_id'])
            if pair:
              tTime, offset = get_time(match['region'])
              region = match['region'].replace("_", " ").capitalize()
              embed = discord.Embed(title="Chat found", description=f"You've been matched with **{pair.name}**!\nYou can now start chatting, say hi!\n{config.replycont} Their languages: `{', '.join(match['langs'])}`\n{config.reply} Region: **{region}**\n{config.reply} Their time: <t:{int(tTime)}:t> *GMT{offset} (estimated)*\n\nPair ID: `{pair.id}`", color=discord.Color.green())
              embed.set_author(name=pair.name, icon_url=pair.avatar.url if pair.avatar else pair.default_avatar.url)
              embed.set_footer(text="You can cancel the chat by doing /disconnect")
              await interaction.user.send(embed=embed)
              tTime, offset = get_time(profile['region'])
              region = profile['region'].replace("_", " ").capitalize()
              embed = discord.Embed(title="Chat found", description=f"You've been matched with **{interaction.user.name}**!\nYou can now start chatting, say hi!\n{config.replycont} Their languages: `{', '.join(match['langs'])}`\n{config.replycont} Region: **{region}**\n{config.reply} Their time: <t:{int(tTime)}:t> *GMT{offset} (estimated)*\n\nPair ID: `{interaction.user.id}`", color=discord.Color.green())
              embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
              embed.set_footer(text="You can cancel the chat by doing /disconnect")
              await pair.send(embed=embed)
              break
              
        attempts += 1
        if attempts >= 6:
           embed = discord.Embed(description=f"{config.no} | No partners found, please try again later", color=config.embederrorcolor)
           profile['chat']['waiting'] = False
           profile['chat']['w_pers'] = False
           await interaction.user.send(embed=embed)
           await profile_collection.update_one({"_id": uid}, {"$set": profile}, upsert=True)
           break       
       
        time.sleep(6)
                 
      
      
    except Exception as e:
        logger.error(e)
    
    
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.add_command(command)            