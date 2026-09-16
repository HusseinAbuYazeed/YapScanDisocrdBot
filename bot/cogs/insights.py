import discord
from discord import app_commands
from discord.ext import commands

class Insights(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="check if the bot is on")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong")

    @app_commands.command(name="count", description="Count the last 50 messages in this channel")
    async def count(self, interaction: discord.Interaction):
        await interaction.response.defer()
        messages = [msg async for msg in interaction.channel.history(limit=50)]
        await interaction.followup.send(f"Found {len(messages)} messages")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Insights(bot))