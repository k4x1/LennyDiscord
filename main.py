from typing import Final
import os
import json
import aiohttp
from dotenv import load_dotenv
from discord import Intents, Message, Object, app_commands, Interaction, Member
from discord.ext import commands
from responses import get_response, cosmetics
from inspirobot import generate_quote_url

load_dotenv()
# hard coded guild id to bunguin server, makes it easier to test but can replace with global commands in the future
TOKEN: Final[str] = os.environ['DISCORD_TOKEN']
GUILD_ID: Final[int] = 1201426274028101722
API_BASE = "http://headlice-api.bunguin.games:8088"

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
        if response:
            await message.author.send(response)
    else:
        response = get_response(content)
        if response:
            await message.channel.send(response)

#force syncs the slash commands to the server
@bot.event
async def on_ready():
    user = bot.user
    if not user:
        return

    print(f"CrabbyBot is logged in as {user.name} (ID: {user.id})")
    guild = Object(id=GUILD_ID)
    try:
        synced = await bot.tree.sync(guild=guild)
        print(f"Guild slash commands synced: {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync guild commands: {e}")

#join message
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
    await process_user_message(message, text)
    await bot.process_commands(message)


# /inspireme command, funny inspire bot quote
@bot.tree.command(
    name="inspireme",
    description="Send you a randomly generated InspiroBot quote URL",
    guild=Object(id=GUILD_ID),
)
async def inspireme(interaction: Interaction):
    await interaction.response.defer()
    try:
        quote_url = await generate_quote_url()
        await interaction.followup.send(quote_url)
    except Exception as e:
        await interaction.followup.send(f"Error fetching quote: {e}")

# admin only
# list of available codes can get from the API
@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(
    name="availablecodes",
    description="List all available cosmetic keys",
    guild=Object(id=GUILD_ID),
)
async def available_codes(interaction: Interaction):
    # hardcoded 
    lines = [f"`{key}`: {desc}" for key, desc in cosmetics.items()]
    message = "\n".join(lines)
    await interaction.response.send_message(message, ephemeral=True)

# admin only
# give api reward to different user
@bot.tree.command(
    name="givestuff",
    description="(Admin) Give someone a code for a cosmetic and DM it to them",
    guild=Object(id=GUILD_ID),
)
@app_commands.describe(
    member="The user to give the item to",
    cosmetic_key="The key for the cosmetic item"
)
@app_commands.checks.has_permissions(administrator=True)
async def give_stuff(interaction: Interaction, member: Member, cosmetic_key: str):
    await interaction.response.defer(ephemeral=True)
    payload = {
        "discordUserId": str(member.id),
        "discordUserName": member.name,
        "cosmeticKey": cosmetic_key
    }
    async with aiohttp.ClientSession() as session:
        try:
            resp = await session.post(f"{API_BASE}/api/Voucher/generate", json=payload)
            if resp.status != 200:
                text = await resp.text()
                return await interaction.followup.send(
                    f":x: Failed to generate: {resp.status} {text}", ephemeral=True
                )
            data = await resp.json()
            dm = (
                f"Hi {member.name}! You've been granted a free **{data['cosmeticKey']}**.\n"
                f"Your voucher code is: `{data['code']}`\n"
                f"Expires At: {data['expiresAt']}"
            )
            try:
                await member.send(dm)
                await interaction.followup.send(
                    f":white_check_mark: Sent `{data['cosmeticKey']}` code to {member.mention}.",
                    ephemeral=True
                )
            except Exception:
                await interaction.followup.send(
                    f":warning: Couldn't DM {member.mention}, but code was generated: `{data['code']}`",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)

# redeem codes here
@bot.tree.command(
    name="freestuff",
    description="Get a voucher code for a cosmetic item!",
    guild=Object(id=GUILD_ID),
)
@app_commands.describe(cosmetic_key="The key for your cosmetic item.")
async def free_stuff(interaction: Interaction, cosmetic_key: str):
    url = "http://headlice-api.bunguin.games:8088/api/Voucher/generate"
    payload = {
        "discordUserId": str(interaction.user.id),
        "discordUserName": interaction.user.name,
        "cosmeticKey": cosmetic_key
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    await interaction.response.send_message(
                        f"Failed to fetch code: {resp.status} {text}",
                        ephemeral=True
                    )
                    return
                data = await resp.json()
                await interaction.response.send_message(
                    f"**Voucher Code:** `{data.get('code')}`\n"
                    f"**Cosmetic Key:** `{data.get('cosmeticKey')}`\n"
                    f"**Expires At:** `{data.get('expiresAt')}`\n"
                    f"Created by: `{data.get('createdBy')}`",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"Error posting to API: {e}",
                ephemeral=True
            )
            
def main() -> None:
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
