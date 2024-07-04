import mysql.connector
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import logging
from mysql.connector import Error
from main import serverId, testServerId
from connect import connectToDatabase
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

    @nextcord.slash_command(name="button", description="Faza testowa buttonów", guild_ids=[testServerId, serverId])
    async def button(self, interaction: Interaction):
        logging.info("Slash command /button called.")
        try:
            mysqlCreateTableRoles = f"""
                CREATE TABLE IF NOT EXISTS roles (
                RoleID BIGINT NOT NULL AUTO_INCREMENT,
                Discord_role_id BIGINT NOT NULL,
                Role_name VARCHAR(255) NOT NULL,
                PRIMARY KEY(RoleID)
                UNIQUE (Discord_role_id)
            );
            """
            connection = connectToDatabase()
            cursor = connection.cursor()
            cursor.execute(mysqlCreateTableRoles)
        except Error as e:
            print(f"Problem with database: {e}")
        finally:
            if connection.is_connected():
                checkTableExists = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'maturaBot' AND table_name = 'roles';"
                cursor.execute(checkTableExists)
                count = cursor.fetchone()
                if count == 0:
                    for role in interaction.guild.roles:
                        cursor.execute(f"""
                        INSERT INTO roles (Discord_role_id, Role_name)
                        VALUES (%s, %s)
                        """, (role.id, role.name))
                        connection.commit()
                        # print(f"Role Id: {role.id}, Role Name: {role.name}")
                    cursor.close()
                    connection.close()
                    # await interaction.response.send_message("Done")
                    print("Connection has been closed")
            
        view = RoleButtons(interaction.guild)
        await interaction.response.send_message("Choose a role:", view=view)

def setup(client):
    client.add_cog(UI(client))