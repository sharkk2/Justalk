import discord
from core.logger.logger import logger

class ProfileMenu(discord.ui.View):
  def __init__(self, interaction, bot):
      super().__init__(timeout=None)
      self.interaction = interaction
      self.bot = bot  
              
  @discord.ui.button(label=f'Change region', style=discord.ButtonStyle.primary, row=1, disabled=False, emoji='🌍')
  async def cRegion(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            ...
       except Exception as e:
          logger.error(e)   
      
          
  @discord.ui.button(label=f'Change language', style=discord.ButtonStyle.primary, row=1, disabled=False, emoji='🗣')
  async def cLang(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            ...
       except Exception as e:
          logger.error(e)                
      
      
  @discord.ui.button(label=f'Toggle invisibilty', style=discord.ButtonStyle.gray, row=2, disabled=False)
  async def tInvis(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            ...
       except Exception as e:
          logger.error(e)   
