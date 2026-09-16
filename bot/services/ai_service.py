from google import genai
from config.settings import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


async def ask_ai(prompt: str) -> str:
    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"AI error: {e}"