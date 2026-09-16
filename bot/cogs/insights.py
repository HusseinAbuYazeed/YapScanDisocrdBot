import re
import discord
from discord import app_commands
from discord.ext import commands
from collections import Counter

STOPWORDS = {
    # English
    "the", "a", "an", "is", "it", "to", "and", "in", "of", "on",
    "i", "you", "he", "she", "we", "they", "im", "u", "ur",

    # Arabic (formal)
    "و", "في", "من", "على", "عن", "إلى", "الى", "أن", "ان",
    "هذا", "هذه", "ذلك", "التي", "الذي", "كل", "بعد", "قبل",

    # Egyptian pronouns / basics
    "ده", "دي", "دة", "كده", "كدا", "انا", "انت", "انتي", "احنا",
    "هو", "هي", "هما", "دول", "ده", "بتاعي", "بتاعك", "بتاعه",

    # Egyptian fillers / common words
    "مش", "بس", "يسطا", "لا", "ايه", "يا", "او", "علي",
    "بقى", "بقا", "عشان", "علشان", "لان", "لأن", "برضو",
    "طيب", "خلاص", "يعني", "كمان", "فعلا", "اصل", "اه",
    "ايوه", "لسه", "دلوقتي", "هنا", "هناك", "كده كده",
    "ممكن", "لازم", "عايز", "عايزة", "عاوز", "عاوزة",
    "حد", "حاجة", "حاجه", "كام", "فين", "امتى", "ليه",
    "ازاي", "مين", "شوية", "شويه", "خالص", "اوي", "جدا",

    # Common short interjections
    "هههه", "ههه", "هه", "لول", "واو", "ok", "okay", "yes", "no",
}

EMOJI_PATTERN = re.compile(
    r"<a?:\w+:\d+>"      # custom server emoji: <:name:id> or <a:name:id>
    r"|:\w+:"            # colon-style: :name:
    r"|["
    r"\U0001F300-\U0001FAFF"
    r"\U00002700-\U000027BF"
    r"\U0001F1E0-\U0001F1FF"
    r"]+"
)


class Insights(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check if the bot is online")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong! 🏓")

    @app_commands.command(name="count", description="Count the last 50 messages in this channel")
    async def count(self, interaction: discord.Interaction):
        await interaction.response.defer()
        messages = [msg async for msg in interaction.channel.history(limit=50)]
        oldest = messages[-1].created_at.strftime("%Y-%m-%d %H:%M") if messages else "N/A"
        await interaction.followup.send(f"Found {len(messages)} messages, oldest one from: {oldest}")

    @app_commands.command(name="topwords", description="Show most used words (whole channel or a specific member)")
    async def topwords(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer()
        messages = [msg async for msg in interaction.channel.history(limit=2500)]

        all_words = []
        for msg in messages:
            if msg.author.bot:
                continue
            if member is not None and msg.author.id != member.id:
                continue
            content = EMOJI_PATTERN.sub("", msg.content)
            words = content.lower().split()
            words = [w for w in words if w not in STOPWORDS]
            all_words.extend(words)

        word_counts = Counter(all_words)
        top_5 = word_counts.most_common(5)

        result = "\n".join(f"{word}: {count}" for word, count in top_5)
        title = f"Top words for {member.display_name}" if member else "Top words in this channel"
        await interaction.followup.send(f"{title}:\n{result}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Insights(bot))