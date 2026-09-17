import re
import discord
from discord import app_commands
from discord.ext import commands
from collections import Counter
from bot.services.ai_service import ask_ai

STOPWORDS = {
    # English
    "the", "a", "an", "is", "it", "to", "and", "in", "of", "on",
    "i", "you", "he", "she", "we", "they", "im", "u", "ur", "thx", "pls", "please", "bro", "dude", "lol", "ok", "okay", "yes", "no",

    # Arabic (formal & classical)
    "و", "في", "من", "على", "عن", "إلى", "الى", "أن", "ان","الله",
    "هذا", "هذه", "ذلك", "التي", "الذي", "كل", "بعد", "قبل",
    "مع", "بين", "تحت", "فوق", "غير", "هو", "هي", "هما", "هن", "نحن",
    "أنت", "انت", "أنتم", "أنتم", "هؤلاء", "ذلك", "تلكم", "هكم",
    "الذين", "اللواتي", "اللاتي", "حين", "حيث", "إذا", "إذاً", "اذا",
    "أيضاً", "ايضا", "أيضا", "بل", "لكن", "لكنه", "لكنها", "لذلك", "هكذا","لسا","لما","بجد",
    "نعم", "لا", "ما", "منذ", "حتى", "كي", "لكي", "فإن", "فان","ال","عامل","وانا",
    "ولو", "أو", "أم", "أين", "كيف", "متى", "لماذا", "كم",
    "بعض", "أغلب", "معظم", "سوف", "قد", "لقد", "بل", "إنما",

    # Egyptian pronouns, basics & demonstratives
    "ده", "دي", "دة", "كده", "كدا", "انا", "انت", "انتي", "احنا",
    "هما", "دول", "بتاعي", "بتاعك", "بتاعه", "بتاعتي", "بتاعتك", "بتاعته",
    "بتاعتنا", "بتوع", "بتوعي", "عندي", "عندك", "عنده", "عندها", "عندنا",
    "معايا", "معاك", "معاه", "معاها", "معانا", "جوه", "بره", "قدام", "ورا","ولا", "ي", "فشخ",

    # Egyptian fillers, slang & common conversational words
    "مش", "بس", "يسطا", "ياسطا", "ايه", "يا", "او", "علي",
    "بقى", "بقا", "عشان", "علشان", "لان", "لأن", "برضو",
    "طيب", "خلاص", "يعني", "كمان", "فعلا", "اصل", "أصل", "اه",
    "ايوه", "لسه", "دلوقتي", "دلوقت", "دلوئتي", "هنا", "هناك", "كده كده",
    "ممكن", "لازم", "عايز", "عايزة", "عاوز", "عاوزة",
    "حد", "حاجة", "حاجه", "كام", "فين", "امتى", "ليه",
    "ازاي", "مين", "شوية", "شويه", "خالص", "اوي", "أوي", "قوي", "جدا",
    "طب", "فا", "فـ", "قاعد", "قاعدين", "شغال", "رايح", "جاي",
    "بيقول", "بتقول", "عارف", "عارفة", "فاهم", "فاهمة", "شايف", "شايفة",
    "تاني", "تانية", "تانيين", "زي", "اللى", "اللي", "كذا",
    "طبعاً", "طبعا", "أساساً", "اساساً", "اساسا", "عموماً", "عموما",
    "مفيش", "مافيش", "شكراً", "شكرا", "حبيبي", "ياعم", "يا عم", "باشا",
    "يا باشا", "يا صاحبي", "لو سمحت", "ياريت", "يا ريت", "يلا",
    "اصلا", "أصلا", "امين", "أمين", "تمام", "ماشي", "قشطة", "قشطه",
    "فل", "عسل", "حلو", "حلوة", "حلوه", "وحش", "وحشة", "وحشه",
    "بالظبط", "بالضبط", "عادي", "جديد", "قديم", "غالباً", "غالبا",
    "أكيد", "اكيد", "بيقولك", "تقولك", "بيقولوا", "تقريبًا", "تقريبا",
    "بص", "بصي", "شوف", "شوفي", "اسمع", "اسمعي", "فكك", "كبر",
    "سيبك", "طنش", "ياعمي", "ياخي", "يا خويا", "يا زميلي", "زميلي",
    "يابني", "يابنتي", "حاج", "كابتن", "استاذ", "معلم", "برنس", "ريس",
    "نجم", "بطل", "جميل", "اخويا", "أخويا", "اختي", "أختي", "جماعة",
    "يا جماعة", "ياجماعة", "شباب", "يا شباب", "بنات", "يا بنات",
    "الناس", "ناس", "بني ادمين", "الكل", "الجميع", "كلهم", "كله",
    "كلها", "كلنا", "كلكم", "جميعاً", "جميعا", "حبة", "حبه",
    "كتير", "كثير", "كتر", "أكتر", "اكتر", "أقل", "اقل",
    "أشياء", "اشياء", "أمور", "امور", "حوار", "حوارات", "موضوع",
    "مواضيع", "قصة", "قصص", "سالفة", "شغل", "شغلانة", "شغلانه",
    "خدمة", "مصلحة", "فكرة", "فكره", "أفكار", "افكار", "سبب",
    "أسباب", "اسباب", "طريقة", "طرق", "حالة", "حالات", "وضع",
    "أوضاع", "اوضاع", "شكل", "أشكال", "اشكال", "نوع", "أنواع",
    "انواع", "جزء", "أجزاء", "اجزاء", "مرة", "مره", "مرات",
    "زمان", "النهاردة", "النهارده", "إمبارح", "امبارح", "بكرة", "بكره",
    "ساعة", "ساعات", "دقيقة", "دقايق", "ثانية", "ثواني", "لحظة",
    "أول", "اول", "أولاً", "اولا", "ثانياً", "ثانيا", "أخيراً", "اخيرا",
    "فالبداية", "في الاخر", "عالفكرة", "عالفكره", "بالمناسبة",
    "ع العموم", "في العموم", "بشكل عام", "بوجه عام", "من الاول",
    "من الأول", "مرة تانية", "مرة تانيه", "من جديد", "من تاني",
    "كمان مرة", "غير كده", "غير كدا", "بالإضافة", "بالاضافة",
    "مع ذلك", "على الرغم", "بالرغم", "مع ان", "رغم ان", "بس كده",
    "بس كدا", "وبس", "لا غير", "مش أكتر", "مش اكتر", "ولا حاجة",
    "ولا حاجه", "ولا اي حاجه", "ولا شيء", "ولا شىء", "مفيش حاجة",
    "مفيش حاجه", "مافيش حاجة", "مافيش حاجه", "مفيش مشكلة", "حصل خير",

    # Common short interjections & laughter variants
    "هههه", "ههه", "هه", "ههههه", "هههههه", "خخخ", "ههخخ", "واو",

    # Verbs of "kaan" and its sisters
    "كان", "كانت", "كنت", "يكون", "تكون", "يكونوا", "نكون", "كنتم", "كنا",
    "بقى", "بقت", "بقيت", "بقينا", "بقوا", "يبدأ", "بدأ", "بدأت",

    # Common conditional/connector particles
    "لو", "لولا", "انما", "أنما", "إنما", "عشان كده", "عشان كدا", "علشان كده",
    "عشان كده", "بسبب", "عن طريق", "من خلال", "من ناحية", "من جهة",

    # Common colloquial verbs that show up in top words
    "روحت", "راح", "راحت", "راحوا", "جيت", "جه", "جت", "جوا", "عملت",
    "عمل", "عملت", "عملوا", "بيعمل", "بتعمل", "بيعملوا", "خدت", "خد", "خدوا",
    "جبت", "جاب", "جابت", "جابوا", "قلت", "قال", "قالت", "قالوا",

    # Oaths and religious expressions
    "والله", "واللهِ", "ربنا", "يا رب", "يارب", "ماشاء الله", "ماشاءالله",
    "إن شاء الله", "ان شاء الله", "الحمد لله", "الحمدلله", "لا حول ولا قوة إلا بالله"
}

EMOJI_PATTERN = re.compile(
    r"<a?:\w+:\d+>"           # custom server emoji: <:name:id> or <a:name:id>
    r"|:\w+:"                 # colon-style: :name:
    r"|["
    r"\U0001F600-\U0001F64F"  # emoticons (faces)
    r"\U0001F300-\U0001F5FF"  # symbols & pictographs
    r"\U0001F680-\U0001F6FF"  # transport & map
    r"\U0001F1E0-\U0001F1FF"  # flags
    r"\U00002600-\U000026FF"  # misc symbols
    r"\U00002700-\U000027BF"  # dingbats
    r"\U0001F900-\U0001F9FF"  # supplemental symbols
    r"\U0001FA70-\U0001FAFF"  # extended symbols
    r"]"
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

            content = re.sub(r"https?://\S+|www\.\S+", "", msg.content)
            content = re.sub(r"<@!?\d+>|<#\d+>|<@&\d+>", "", content)  # mentions, channels, roles
            content = EMOJI_PATTERN.sub("", content)

            words = re.findall(r"[\w\u0600-\u06FF]+", content.lower())
            words = [
                w for w in words
                if w not in STOPWORDS
                and not w.isdigit()
                and len(w) >= 2
            ]
            all_words.extend(words)

        word_counts = Counter(all_words)
        top_10 = word_counts.most_common(10)

        result = "\n".join(f"{word}: {count}" for word, count in top_10)
        title = f"Top words for {member.display_name}" if member else "Top words in this channel"
        await interaction.followup.send(f"{title}:\n{result}")

    @app_commands.command(name="topemojis", description="Show most used emojis (whole channel or a specific member)")
    async def topemojis(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer()
        messages = [msg async for msg in interaction.channel.history(limit=1000)]

        all_emojis = []
        for msg in messages:
            if msg.author.bot:
                continue
            if member is not None and msg.author.id != member.id:
                continue
            found = EMOJI_PATTERN.findall(msg.content)
            all_emojis.extend(found)

        emoji_counts = Counter(all_emojis)
        top_10 = emoji_counts.most_common(10)

        result = "\n".join(f"{emoji}: {count}" for emoji, count in top_10)
        title = f"Top emojis for {member.display_name}" if member else "Top emojis in this channel"
        await interaction.followup.send(f"{title}:\n{result}")

    @app_commands.command(name="asktest", description="Test AI connection")
    async def asktest(self, interaction: discord.Interaction):
        await interaction.response.defer()
        reply = await ask_ai("Say hello in one short sentence")
        await interaction.followup.send(reply)

    @app_commands.command(name="summarize", description="Summarize the last N messages in this channel")
    @app_commands.checks.cooldown(1, 3600)  # once per hour, per user
    async def summarize(self, interaction: discord.Interaction, amount: int = 2000):
        await interaction.response.defer()

        if amount < 10:
            amount = 10
        if amount > 3000:
            amount = 3000

        messages = [msg async for msg in interaction.channel.history(limit=amount)]
        messages.reverse()

        lines = []
        for msg in messages:
            if msg.author.bot:
                continue
            if not msg.content:
                continue
            lines.append(f"{msg.author.display_name}: {msg.content}")

        chat_text = "\n".join(lines)

        prompt = (
    "Summarize this Discord conversation topic by topic, in its original language "
    "(Arabic/Egyptian Arabic or English).\n\n"
    "For each topic, provide a brief summary focusing on the key points rather than full details.\n\n"
    "Format:\n"
    "Topic 1: (key points)\n"
    "Topic 2: (key points)\n\n"
    "Cover all topics individually without merging them together.\n\n"
    f"Conversation:\n{chat_text}"
)

        summary = await ask_ai(prompt)

        if len(summary) > 1900:
            summary = summary[:1900] + "..."

        await interaction.followup.send(f"📋 Summary of the last {len(messages)} messages:\n\n{summary}")

    @summarize.error
    async def summarize_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"Slow down — you can use this command again in {error.retry_after:.0f} seconds",
                ephemeral=True
            )

    @app_commands.command(name="roast", description="Get a lighthearted roast/opinion on the last topic discussed")
    @app_commands.checks.cooldown(1, 3600)  # once per hour, per user
    async def roast(self, interaction: discord.Interaction, amount: int = 50):
        await interaction.response.defer()

        if amount < 5:
            amount = 5
        if amount > 300:
            amount = 300

        messages = [msg async for msg in interaction.channel.history(limit=amount)]
        messages.reverse()

        lines = []
        for msg in messages:
            if msg.author.bot:
                continue
            if not msg.content:
                continue
            lines.append(f"{msg.author.display_name}: {msg.content}")

        chat_text = "\n".join(lines)

        prompt = (
    "You are that brutally sarcastic, zero-chill friend in the Discord group who roasts everyone without mercy, BUT WITHOUT using any bad words or profanity. "
    "Read the last messages and drop a ruthless, witty comment. "
    "Expose their bad logic, roast whoever said something dumb, and keep it painfully funny. "
    "Keep it very short (2-3 lines max), pure chaotic energy, absolutely no formal summary or swear words. "
    "Reply in the same language/dialect as the chat (mostly Egyptian Arabic Franco/slang).\n\n"
    f"Conversation:\n{chat_text}"
)
        reply = await ask_ai(prompt)

        if len(reply) > 1900:
            reply = reply[:1900] + "..."

        await interaction.followup.send(f"🔥 {reply}")

    @roast.error
    async def roast_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"Slow down — you can use this command again in {error.retry_after:.0f} seconds",
                ephemeral=True
            )
async def setup(bot: commands.Bot):
    await bot.add_cog(Insights(bot))