import discord
from discord.ext import commands


def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(
        command_prefix="!",
        intents=intents
    )

    @bot.event
    async def setup_hook():
        await bot.load_extension("bot.cogs.insights")

    @bot.event
    async def on_ready():
        print(f"{bot.user} is online!")
        try:
            guild = discord.Object(id=1489873713691099177)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild")
        except Exception as e:
            print(f"Sync failed: {e}")   

    return bot