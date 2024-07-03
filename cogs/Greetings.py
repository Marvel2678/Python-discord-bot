import mysql.connector
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from connect import connection
from mysql.connector import Error
class Greetings(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello! I hope you have a good day!")
    
    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        try:
            mysqlCreateTable = f"""
            CREATE TABLE IF NOT EXISTS users (
                Id INT(15) NOT NULL AUTO_INCREMENT,
                Discord_id INT(15) NOT NULL,
                Name VARCHAR(255) NOT NULL,
                PRIMARY KEY(Id)
            );
            """
            cursor = connection.cursor()
            cursor.execute(mysqlCreateTable)
            
            cursor.execute(f"""
            INSERT INTO users (Discord_id, Name)
            VALUES (%s, %s)
            """, (member.id, member.name))
            connection.commit()
        except Error as error:
            print(f"Error: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

            
        channel = self.client.get_channel(1252620757125693601)
        message = f"Witaj {member.name}! Jako główny bot tego serwera życzę ci miłej pracy wśród nas nad maturą."
        embed = nextcord.Embed(
            title="Witaj na serwerze!", 
            description=message, 
            color=0xFF5733
        )
        embed.set_footer(
            text="Powodzenia! Administratorzy bota i serwera!", 
            icon_url="https://cdn-icons-png.flaticon.com/512/25/25231.png"
        )
        await member.send(embed = embed)
        if channel:
            await channel.send(f"Hello {member.name}! Welcome to the server!")
            # await member.add_role
        else:
            print("Channel not found or bot lacks permission to access the channel.")
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(1252622727022514246)
        if channel:
            await channel.send(f"Goodbye {member.name} :(. We hope you come back to us soon!")
        else:
            print("Channel not found or bot lacks permission to access the channel.") 
    
    #Slash commands  
    # @nextcord.slash_command(name="Test", description="Testowa komenda", guild_ids=[testSerwer])
    # async def test(self, interaction: Interaction):
    #     await interaction.response.send_message("Witaj, to testowa komenda!") 

def setup(client):
    client.add_cog(Greetings(client))
