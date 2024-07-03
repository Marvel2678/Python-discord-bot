import mysql.connector
from mysql.connector import Error
import logging
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import logging
from dotenv import load_dotenv
import os
from connect import connection

logging.basicConfig(level=logging.INFO)

class DB(commands.Cog):
    def __init__(self, client):
        self.client = client

    load_dotenv("../")
    serverId = int(os.getenv("SERVER_ID"))
    testServerId = int(os.getenv("TEST_SERVER_ID"))
    
    @nextcord.slash_command(name="store_sheet", description="Store important data to database", guild_ids=[serverId, testServerId])
    async def store_sheet(self, interaction: Interaction, role: nextcord.Role, sheet: str):
        guild_id = interaction.guild.id
        try:
            mysqlCreateTable = f"""
            CREATE TABLE IF NOT EXISTS sheets (
                Id INT(15) NOT NULL AUTO_INCREMENT,
                Sheet VARCHAR(255) NOT NULL,
                Role VARCHAR(255) NOT NULL,
                PRIMARY KEY(Id)
            );
            """
            cursor = connection.cursor()
            cursor.execute(mysqlCreateTable)
            print(f"New table DB_{guild_id} has been created successfully!")
        except Error as e:
            print(f"Failed to create table in MySQL Database! Reason: {e}")
        finally:
            if connection.is_connected():
                table = f"DB_{guild_id}"
                mysqlInsertRow = f"INSERT INTO {table} (User, Arkusz, Status) VALUES (%s, %s, 0);"
                mysqlInsertRowValues = (str(interaction.user), sheet)
                cursor.execute(mysqlInsertRow, mysqlInsertRowValues)
                
                connection.commit()
                
                await interaction.response.send_message("Message has been stored in Database!")
                
                cursor.close()
                connection.close()
                
                print("Connection has been closed")

    @nextcord.slash_command(name="view_store", description="View all data in this server", guild_ids=[serverId, testServerId])
    async def view_store(self, interaction: Interaction, user: nextcord.Member):
        guild = interaction.guild.id
        try:
            mysqlGetAllDataFromGuild = f"SELECT * FROM DB_{guild} WHERE User=%s;"
            cursor = connection.cursor()
            cursor.execute(mysqlGetAllDataFromGuild, (str(user),))
            results = cursor.fetchall()
            if results:
                message = f"Data for {user.display_name}:\n"
                for row in results:
                    status_emoji = ":x:" if row[3] == 0 else ":white_check_mark:"
                    message += f"{row[0]}. {row[2]}, \nStatus: {status_emoji}\n\n"
                await interaction.response.send_message(message)
            else:
                await interaction.response.send_message(f"No data found for {user.display_name}")
        except Error as e:
            logging.error(f"Database error: {e}")
            await interaction.response.send_message(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @nextcord.slash_command(name="change_stat", description="Change status to the done or no done", guild_ids=[serverId, testServerId])
    async def change_stat(self, interaction: Interaction, id: int):
        guild = interaction.guild.id
        try:
            mysqlDataToUpdate = f"SELECT status FROM DB_{guild} WHERE Id=%s;"
            cursor = connection.cursor()
            cursor.execute(mysqlDataToUpdate, (id,))
            result = cursor.fetchone()
            
            if result:
                actualStatus = 1 if result[0] == 0 else 0
                mysqlUpdateStatus = f"UPDATE DB_{guild} SET status=%s WHERE Id=%s;"
                cursor.execute(mysqlUpdateStatus, (actualStatus, id))
                connection.commit()  # Don't forget to commit the transaction
                await interaction.response.send_message("Status updated successfully!")
            else:
                await interaction.response.send_message("No record found with the given Id.")
        except Error as e:
            logging.error(f"Database error: {e}")
            await interaction.response.send_message(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
def setup(client):
    client.add_cog(DB(client))
