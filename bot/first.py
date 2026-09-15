import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()

# to make the bot able to handle messages
intents.message_content = True

# make a bot object
bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online")

    await bot.tree.sync()

    print("Slash commands synced!")


@bot.tree.command(
    name="analyze",
    description="Analyze the chat"
)
async def analyze(interaction: discord.Interaction):

    channel = interaction.channel

    async for message in channel.history(limit=100):
        print(message.author, ":", message.content)

    await interaction.response.send_message(
        "I collected the messages!"
    )
    
bot.run(TOKEN)