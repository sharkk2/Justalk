import discord
from discord.ext import commands
import config
import time
     
class onMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild:
            return
        
        if message.author.bot:
            return
        
        if message.content.startswith("~") and message.content.endswith("~"):
            return
        
        user = message.author
        uid = str(user.id)
        now = time.time()
        if uid in self.cooldowns and now - self.cooldowns[uid] < 2:
            message.add_reaction("⏳")
            return
        
        self.cooldowns[uid] = now
        
        db = self.bot.mongoConnect['Justalk']
        profile_collection = db["profiles"]    
        profile = await profile_collection.find_one({"_id": uid})
        if profile['chat']['chatting']:
            partner = profile['chat']['partner']
            if partner:
                chatter = await self.bot.fetch_user(int(partner))
                if chatter:
                    
                    blacklist = ["http://", "https://", "www.", ".com", ".net", ".org", ".io", ".co", ".me", ".gg", ".dev"]
                    if any(word in message.content for word in blacklist):
                      await message.add_reaction(config.no)
                      return
                    
                    await chatter.send(f"**{user.name}**: {message.content}")
                    await message.add_reaction("📩")    
         
async def setup(bot):
    await bot.add_cog(onMessage(bot))         