from typing import Final
import os
import json
from dotenv import load_dotenv
from discord import Intents, Message, app_commands, Interaction
from discord.ext import commands
from responses import get_response
from inspirobot import generate_quote_url

load_dotenv()

TOKEN: Final[str] = os.environ['DISCORD_TOKEN']

intents = Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def process_user_message(message: Message, content: str) -> None:
    """Handle text commands (sync get_response)."""
    if not content:
        print("No content to send.")
        return

    if content.startswith('?'):
        response = get_response(content[1:])
        await message.author.send(response)
    else:
        response = get_response(content)
        await message.channel.send(response)


@bot.event
async def on_ready():
    user = bot.user
    if user is None:
        return
    print(f'CrabbyBot is logged in as {user.name} (ID: {user.id})')
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.event
async def on_member_join(member):
    try:
        await member.send(
            "Welcome to the server! :tada: \nGet free stuff by typing /freestuff <cosmetic key>"
        )

        print(f"Sent a welcome DM to {member}")
    except Exception as e:
        print(f"Couldn't send DM to {member}: {e}")


@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return

    text = message.content.strip()
    lower = text.lower()

    if any(tok in lower for tok in (':)', 'lol', 'haha', 'quote')):
        try:
            quote_url = await generate_quote_url()
            await message.channel.send(quote_url)
        except Exception as e:
            await message.channel.send(f"Error fetching quote: {e}")
        return

    print(f'[{message.channel}] {message.author}: "{text}"')
    await process_user_message(message, text)

    await bot.process_commands(message)


@bot.tree.command(name="freestuff", description="Preview the API JSON POST")
@app_commands.describe(cosmetic_key="The key for your cosmetic item.")
async def getpost(interaction: Interaction, cosmetic_key: str):
    payload = {
        "discordUserId": str(interaction.user.id),
        "username": interaction.user.name,
        "cosmeticKey": cosmetic_key
    }
    pretty_json = json.dumps(payload, indent=2)
    await interaction.response.send_message(
        f"**Test POST payload:**\n"
        f"**Username:** `{interaction.user.name}`\n"
        f"```json\n{pretty_json}\n```\n"
        f"no endpoint set yet post to api here)",
        ephemeral=True)


def main() -> None:
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
