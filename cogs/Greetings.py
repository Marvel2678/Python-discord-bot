import mysql.connector
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from connect import connectToDatabase
from mysql.connector import Error
class Greetings(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello! I hope you have a good day!")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            mysqlCreateTable = f"""
                CREATE TABLE IF NOT EXISTS users (
                UserID BIGINT NOT NULL AUTO_INCREMENT,
                Discord_user_id BIGINT NOT NULL,
                User_name VARCHAR(255) NOT NULL,
                PRIMARY KEY(UserID),
                UNIQUE (Discord_user_id)
                );
                """
            connection = connectToDatabase()
            cursor = connection.cursor()
            cursor.execute(mysqlCreateTable)
            
            checkUserExist = "SELECT COUNT(*) FROM users WHERE Discord_user_id=%s"
            cursor.execute(checkUserExist, (member.id,))
            userExists = cursor.fetchone()[0]

            if userExists == 0:
                insertUser = f"""
                INSERT INTO users (Discord_user_id, User_name)
                VALUES (%s, %s)
                """
                cursor.execute(insertUser, (member.id, member.name))
                connection.commit()
        
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
            await member.send(embed=embed)

            if channel:
                await channel.send(f"Hello {member.name}! Welcome to the server!")
            else:
                print("Channel not found or bot lacks permission to access the channel.")
        except Error as error:
            print(f"Error: {error}")
        
        finally:
            if connection.is_connected():
                
                connection.close()
                cursor.close()

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
