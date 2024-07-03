import mysql.connector
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from mysql.connector import Error
from dotenv import load_dotenv
import os
load_dotenv("../")
class LevelSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # testServerId = int(os.getenv("TEST_SERVER_ID"))
    # @nextcord.slash_command(name="update sheet status", description="this command is updating sheet status", guild_ids=testServerId)
    # async def updateSheetStatus(self, interaction: Interaction):
    #     await interaction.response.send_message("test")
        
def setup(client):
    client.add_cog(LevelSystem(client))