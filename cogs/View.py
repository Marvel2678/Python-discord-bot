import mysql.connector
from mysql.connector import Error
import logging
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import logging

logging.basicConfig(level=logging.INFO)

class View(commands.Cog):
    def __init__(self, client):
        self.client = client

    testServerId = 1141070071616245940

    # @nextcord.slash_command(name="show_db", description="View all data in this server", guild_ids=[testServerId])
    # async def show_db(self, interaction: Interaction, user: nextcord.Member):
    #     guild = interaction.guild.id
    #     try:
    #         connection = mysql.connector.connect(
    #             host="localhost",
    #             user"word='',
    #             database='maturaBot'
    #         )
    #         mysqlGetAllDataFromGuild = f"SELECT * FROM DB_{guild} WHERE User=%s;"
    #         cursor = connection.cursor()
    #         cursor.execute(mysqlGetAllDataFromGuild, (str(user),))
    #         results = cursor.fetchall()
    #         if results:
    #             message = f"Data for {user}:\n"
    #             for row in results:
    #                 message += f"Id: {row[0]}, Arkusz: {row[2]}, Status: {row[3]}\n"
    #             await interaction.response.send_message(message)
    #         else:
    #             await interaction.response.send_message(f"No data found for {user}")
    #     except Error as e:
    #         await interaction.response.send_message(f"Error: {e}")
    #     finally:
    #         if connection.is_connected():
    #             cursor.close()
    #             connection.close()


def setup(client):
    client.add_cog(View(client))
