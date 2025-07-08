from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.members = True 
intents.message_content = True  
client: Client = Client(intents=intents)    
#bot = commands.Bot(command_prefix="!", intents=intents)


async def send_message(message: Message, content: str) -> None:
    if not content:
        print("No content to send.")
        return
    
    if is_private := content[0] == '?':
        content = content[1:]
        try:
            response: str = get_response(content)
            await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception as e:
            print(e)


@client.event
async def on_ready():
     print(f'Bot is ready! Logged in as {client.user.name} (ID: {client.user.id})')

@client.event
async def on_member_join(member):
    try:
        await member.send(
            "Welcome to the server! 🎉\n"
            #"Want some free stuff? Just DM me `/freestuff` and I’ll hook you up with a redemption code!"
        )
        print(f"Sent a welcome DM to {member}")
    except Exception as e:
        print(f"Couldn't send DM to {member}: {e}")

@client.event
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()