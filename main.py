import nextcord
from nextcord.ext import commands
import os
from nextcord import Interaction
import logging
from dotenv import load_dotenv

load_dotenv()
serverId = int(os.getenv("SERVER_ID"))
testServerId = int(os.getenv("TEST_SERVER_ID"))
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

logging.basicConfig(level=logging.INFO)
intents = nextcord.Intents.all()

client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="twoich komend"))
    logging.info(f'Logged in as {client.user}')
    logging.info("The bot is active now!")

async def load_extensions():
    try:
        initial_extensions = [f"cogs.{filename[:-3]}" for filename in os.listdir('./cogs') if filename.endswith('.py')]
        
        for extension in initial_extensions:
            client.load_extension(extension)
            logging.info(f"{extension} cog loaded successfully")
    except Exception as e:
        logging.error(f"Failed to load extensions: {e}")

@client.event
async def on_connect():
    await load_extensions()

if __name__ == "__main__":
    client.run(BOT_TOKEN)
