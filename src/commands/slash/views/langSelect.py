import discord
import config
from .regionSelect import regionSelect
from core.logger.logger import logger

class Dropper(discord.ui.Select):
    def __init__(self, profile, bot, interaction):
        self.profile = profile
        self.bot = bot
        self.interaction = interaction
        
        options = [
            discord.SelectOption(label='English', description='English', emoji='🇬🇧', value='en'),
            discord.SelectOption(label='Spanish', description='Español', emoji='🇪🇸', value='es'),
            discord.SelectOption(label='Mandarin', description='普通话', emoji='🇨🇳', value='zh'),
            discord.SelectOption(label='Hindi', description='हिन्दी', emoji='🇮🇳', value='hi'),
            discord.SelectOption(label='Arabic', description='العربية', emoji='🇸🇦', value='ar'),
            discord.SelectOption(label='Bengali', description='বাংলা', emoji='🇧🇩', value='bn'),
            discord.SelectOption(label='Portuguese', description='Português', emoji='🇧🇷', value='pt'),
            discord.SelectOption(label='Russian', description='Русский', emoji='🇷🇺', value='ru'),
            discord.SelectOption(label='Japanese', description='日本語', emoji='🇯🇵', value='ja'),
            discord.SelectOption(label='Punjabi', description='ਪੰਜਾਬੀ', emoji='🇮🇳', value='pa'),
            discord.SelectOption(label='German', description='Deutsch', emoji='🇩🇪', value='de'),
            discord.SelectOption(label='Javanese', description='ꦧꦱꦗꦮ', emoji='🇮🇩', value='jv'),
            discord.SelectOption(label='Korean', description='한국어', emoji='🇰🇷', value='ko'),
            discord.SelectOption(label='French', description='Français', emoji='🇫🇷', value='fr'),
            discord.SelectOption(label='Turkish', description='Türkçe', emoji='🇹🇷', value='tr'),
            discord.SelectOption(label='Vietnamese', description='Tiếng Việt', emoji='🇻🇳', value='vi'),
            discord.SelectOption(label='Italian', description='Italiano', emoji='🇮🇹', value='it'),
            discord.SelectOption(label='Polish', description='Polski', emoji='🇵🇱', value='pl'),
            discord.SelectOption(label='Ukrainian', description='Українська', emoji='🇺🇦', value='uk'),
            discord.SelectOption(label='Persian', description='فارسی', emoji='🇮🇷', value='fa'),       
            discord.SelectOption(label='Dutch', description='Nederlands', emoji='🇳🇱', value='nl'),
            discord.SelectOption(label='Romanian', description='Română', emoji='🇷🇴', value='ro'),
            discord.SelectOption(label='Hungarian', description='Magyar', emoji='🇭🇺', value='hu'),
        ]


        
        super().__init__(placeholder='Pick your languages', options=options, min_values=1, max_values=5)

    async def callback(self, interaction: discord.Interaction):
        try:
          langs = self.values
          self.profile['langs'] = langs
          
          embed = discord.Embed(title="New profile", description=f"Great! You've picked the following language(s): `{', '.join(langs)}`\nNow, please pick your region", color=config.embedcolor)
          await interaction.response.edit_message(embed=embed, view=regionSelect(self.profile, self.bot, self.interaction))          
                     
        except Exception as e:
            logger.error(e)
            
class langSelect(discord.ui.View):
    def __init__(self, profile, bot, interaction):
        super().__init__(timeout=None) 
        self.add_item(Dropper(profile, bot, interaction))