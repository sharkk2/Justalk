from discord.ext import commands
import discord
import config
import time

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
       latency = round(self.bot.latency * 1000)  
       uptime = int(time.time() - self.bot.startTime)
       hours, r = divmod(uptime, 3600)
       
       embed = discord.Embed(description=f"**Pong** 🏓!\n> Latency: `{latency}`ms\n> Uptime: `{hours}` hours", color=config.embedcolor)
       await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
