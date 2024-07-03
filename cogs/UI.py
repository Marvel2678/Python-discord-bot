import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import logging

logging.basicConfig(level=logging.INFO)

class RoleButtons(nextcord.ui.View):
    def __init__(self, guild):
        super().__init__()
        self.guild = guild

    async def add_or_remove_role(self, interaction: Interaction, role_name: str):
        user = interaction.user
        role = nextcord.utils.get(self.guild.roles, name=role_name)
        
        if role is None:
            await interaction.response.send_message(f"Role '{role_name}' not found!", ephemeral=True)
            return
        
        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(f"Role '{role.name}' removed!", ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.response.send_message(f"Role '{role.name}' added!", ephemeral=True)

    @nextcord.ui.button(label="Matemaksy", style=nextcord.ButtonStyle.primary)
    async def add_role_matemaksy(self, button: nextcord.ui.Button, interaction: Interaction):
        await self.add_or_remove_role(interaction, "matemaksy")

    @nextcord.ui.button(label="Infa", style=nextcord.ButtonStyle.red)
    async def add_role_informatyka(self, button: nextcord.ui.Button, interaction: Interaction):
        await self.add_or_remove_role(interaction, "infa")

    @nextcord.ui.button(label="Fizyka", style=nextcord.ButtonStyle.success)
    async def add_role_fizyka(self, button: nextcord.ui.Button, interaction: Interaction):
        await self.add_or_remove_role(interaction, "fizyka")

    @nextcord.ui.button(label="Biologia", style=nextcord.ButtonStyle.secondary)
    async def add_role_biologia(self, button: nextcord.ui.Button, interaction: Interaction):
        await self.add_or_remove_role(interaction, "biologia")

class UI(commands.Cog):
    def __init__(self, client):
        self.client = client

    testServerId = 1251996857593499789

    @nextcord.slash_command(name="button", description="Faza testowa buttonów", guild_ids=[testServerId])
    async def button(self, interaction: Interaction):
        logging.info("Slash command /button called.")
        view = RoleButtons(interaction.guild)
        await interaction.response.send_message("Choose a role:", view=view)

def setup(client):
    client.add_cog(UI(client))