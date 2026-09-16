import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()

# Make the bot able to read message content
intents.message_content = True

# Make a bot object
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


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

    # Get the current channel
    channel = interaction.channel

    # Collect messages
    messages = []

    async for message in channel.history(limit=100):
        messages.append(message)

    print(f"Collected {len(messages)} messages")

    # Get usernames
    users = []

    for message in messages:
        users.append(message.author.name)

    print(users)

    # Count messages for each user
    user_frequency = {}

    for user in users:

        if user not in user_frequency:
            user_frequency[user] = 1

        else:
            user_frequency[user] += 1

    print(user_frequency)

    # Find the most active user
    most_active_user = max(
        user_frequency,
        key=user_frequency.get
    )

    most_active_count = user_frequency[most_active_user]

    print(
        f"Most active user: {most_active_user}"
    )

    print(
        f"Messages: {most_active_count}"
    )

    # Send result to Discord
    await interaction.response.send_message(
        f"Chat Analysis: \n"
        f"Messages analyzed: {len(messages)}\n"
        f"Most active user: {most_active_user}\n"
        f"Messages: {most_active_count}"
    )


bot.run(TOKEN)