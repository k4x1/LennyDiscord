import aiohttp

API_URL = "https://inspirobot.me/api?generate=true"


async def generate_quote_url() -> str:
  async with aiohttp.ClientSession() as session:
    async with session.get(API_URL) as resp:
      resp.raise_for_status()
      return await resp.text()
  