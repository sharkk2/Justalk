from discord import app_commands
import discord

@app_commands.command(name="test", description="Hello!")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("hello!")
    
async def setup(bot):
    bot.tree.add_command(test)            