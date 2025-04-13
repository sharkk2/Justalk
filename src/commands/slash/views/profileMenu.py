import discord
from core.logger.logger import logger
import config
from .langSelect import langSelect
from .regionSelect import regionSelect

class ProfileMenu(discord.ui.View):
  def __init__(self, interaction, bot):
      super().__init__(timeout=None)
      self.interaction = interaction
      self.bot = bot  
              
  @discord.ui.button(label=f'Change region', style=discord.ButtonStyle.primary, row=1, disabled=False, emoji='🌍')
  async def cRegion(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            embed = discord.Embed(title="Change region", description=f"Choose a region from the dropdown below.", color=config.embedcolor)
            await interaction.response.edit_message(embed=embed, view=regionSelect({}, self.bot, self.interaction, False))
       except Exception as e:
          logger.error(e)   
      
          
  @discord.ui.button(label=f'Change language', style=discord.ButtonStyle.primary, row=1, disabled=False, emoji='🗣')
  async def cLang(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            embed = discord.Embed(title="Change language", description=f"Please pick the language(s) you know, click your first languages first.", color=config.embedcolor)
            await interaction.response.edit_message(embed=embed, view=langSelect({}, self.bot, self.interaction, False))
            
       except Exception as e:
          logger.error(e)                
      
      
  @discord.ui.button(label=f'Toggle anonymity', style=discord.ButtonStyle.gray, row=2, disabled=False)
  async def tInvis(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            db = self.bot.mongoConnect['Justalk']
            profile_collection = db["profiles"]    
            uid = str(interaction.user.id)
            profile = await profile_collection.find_one({"_id": uid})
            
            profile['invisible'] = not profile['invisible']
            await profile_collection.update_one({"_id": str(uid)}, {"$set": profile}, upsert=True)     
            
            region = profile['region'].replace("_", " ").capitalize()
            embed = discord.Embed(title="Profile", description=f"Hello **{interaction.user.name}**\n{config.replycont} Total chats: **{profile['total_chats']}**\n{config.replycont} Current languages: `{', '.join(profile['langs'])}`\n{config.replycont} Current region: **{region}**\n{config.reply} Anonymous: **{profile['invisible']}**", color=config.embedcolor)
            await interaction.response.edit_message(embed=embed, view=ProfileMenu(interaction, self.bot))
       except Exception as e:
          logger.error(e)   
