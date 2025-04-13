import discord
import config
from core.logger.logger import logger

class Dropper(discord.ui.Select):
    def __init__(self, profile, bot, interaction, asSetup):
        self.profile = profile
        self.bot = bot
        self.interaction = interaction
        self.asSetup = asSetup
        
        options = [
            discord.SelectOption(label='Central Europe', description='Germany, Poland, Czechia, etc.', emoji='🌍', value='central_europe'),
            discord.SelectOption(label='Western Europe', description='France, UK, Belgium, Netherlands, etc.', emoji='🌍', value='western_europe'),
            discord.SelectOption(label='Northern Europe', description='Scandinavia, Iceland, Finland, etc.', emoji='🌍', value='northern_europe'),
            discord.SelectOption(label='Southern Europe', description='Italy, Spain, Greece, Portugal, etc.', emoji='🌍', value='southern_europe'),
            discord.SelectOption(label='Eastern Europe', description='Russia, Ukraine, Poland, Hungary, etc.', emoji='🌍', value='eastern_europe'),
            discord.SelectOption(label='Middle East', description='Saudi Arabia, Egypt, Iraq, etc.', emoji='🌍', value='middle_east'),
            discord.SelectOption(label='Southeast Asia', description='Vietnam, Thailand, Indonesia, etc.', emoji='🌏', value='southeast_asia'),
            discord.SelectOption(label='South Asia', description='India, Pakistan, Bangladesh, etc.', emoji='🌏', value='south_asia'),
            discord.SelectOption(label='Central Asia', description='Kazagastan, Uzbekistan, mongolia, etc.', emoji='🌏', value='central_asia'),
            discord.SelectOption(label='Sub-Saharan Africa', description='Kenya, Nigeria, South Africa, etc.', emoji='🌍', value='sub_saharan_africa'),
            discord.SelectOption(label='North Africa', description='Morocco, Algeria, Tunisia, etc.', emoji='🌍', value='north_africa'),
            discord.SelectOption(label='Caribbean', description='Cuba, Jamaica, Dominican Republic, etc.', emoji='🌴', value='caribbean'),
            discord.SelectOption(label='Central America', description='Mexico, Guatemala, Costa Rica, etc.', emoji='🌎', value='central_america'),
            discord.SelectOption(label='Northern america', description='United states, canada, etc', emoji='🌎', value='northen_america'),
            discord.SelectOption(label='Pacific Islands', description='Fiji, Samoa, Tonga, etc.', emoji='🌴', value='pacific_islands'),
        ]

        super().__init__(placeholder='Pick your region', options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        try:  
          region = self.values[0]
          self.profile['region'] = region
          
          
          db = self.bot.mongoConnect['Justalk']
          profile_collection = db["profiles"]    
          uid = str(interaction.user.id)
          profile = await profile_collection.find_one({"_id": uid})
          
          if self.asSetup:
            profile = self.profile
      
            await profile_collection.update_one({"_id": str(uid)}, {"$set": profile}, upsert=True)     
            
            embed = discord.Embed(title="Profile set!", description=f"You're good to go! Start chatting by doing `/chat`", color=config.embedcolor)
            await interaction.response.edit_message(embed=embed, view=None)       
          else:
            from .profileMenu import ProfileMenu
            profile['region'] = region
            await profile_collection.update_one({"_id": str(uid)}, {"$set": profile}, upsert=True)     
            
            region = profile['region'].replace("_", " ").capitalize()
            embed = discord.Embed(title="Profile", description=f"Hello **{interaction.user.name}**\n{config.replycont} Total chats: **{profile['total_chats']}**\n{config.replycont} Current languages: `{', '.join(profile['langs'])}`\n{config.replycont} Current region: **{region}**\n{config.reply} Anonymous: **{profile['invisible']}**", color=config.embedcolor)
            await interaction.response.edit_message(embed=embed, view=ProfileMenu(interaction, self.bot))
                       
                 
                     
        except Exception as e:
            logger.error(e)
            
class regionSelect(discord.ui.View):
    def __init__(self, profile, bot, interaction, asSetup):
        super().__init__(timeout=None) 
        self.add_item(Dropper(profile, bot, interaction, asSetup))