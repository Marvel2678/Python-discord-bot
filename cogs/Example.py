# cogs/example_cog.py

import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class ExampleCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="hello", description="Say hello", guild_ids=[1141070071616245940])
    async def hello(self, interaction: Interaction):
        await interaction.response.send_message("Hello! 👋")

    @nextcord.slash_command(name="ping", description="Check bot latency", guild_ids=[1141070071616245940])
    async def ping(self, interaction: Interaction):
        latency = self.client.latency
        await interaction.response.send_message(f"Pong! Latency: {latency*1000:.2f}ms")

def setup(client):
    client.add_cog(ExampleCog(client))
