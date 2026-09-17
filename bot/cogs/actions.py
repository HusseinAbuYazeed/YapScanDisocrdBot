import discord
from discord import app_commands
from discord.ext import commands


class Actions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="delete_messages", description="Delete the last N messages in this channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def delete_messages(self, interaction: discord.Interaction, amount: int):
        if amount < 1:
            amount = 1
        if amount > 100:
            amount = 100

        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Deleted {len(deleted)} message(s).", ephemeral=True)

    @app_commands.command(name="delete_user_messages", description="Delete the last N messages from a specific member")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def delete_user_messages(self, interaction: discord.Interaction, member: discord.Member, amount: int = 20):
        if amount < 1:
            amount = 1
        if amount > 100:
            amount = 100

        await interaction.response.defer(ephemeral=True)

        def check(msg):
            return msg.author.id == member.id

        deleted = await interaction.channel.purge(limit=200, check=check)
        deleted = deleted[:amount]  # trim in case purge found more than requested before hitting the scan limit
        await interaction.followup.send(
            f"Deleted {len(deleted)} message(s) from {member.display_name}.",
            ephemeral=True
        )

    @delete_messages.error
    @delete_user_messages.error
    async def actions_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You don't have permission to manage messages.", ephemeral=True
            )
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                "I don't have permission to manage messages in this server.", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Actions(bot))