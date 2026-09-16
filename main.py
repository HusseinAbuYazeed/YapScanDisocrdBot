from config.settings import TOKEN
from bot.client import create_bot

bot = create_bot()

bot.run(TOKEN)