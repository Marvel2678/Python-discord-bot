import mysql.connector
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from mysql.connector import Error
from main import serverId, testServerId
from connect import connectToDatabase

class LevelSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name="show_emblemat", description="This command displays the user's sheets.", guild_ids=[testServerId, serverId])
    async def emblemat(self, interaction: Interaction):
        try:
            roles = interaction.user.roles
            embed = nextcord.Embed(title="Emblemat Arkuszy")
            connection = connectToDatabase()
            cursor = connection.cursor()
            user = interaction.user
            checkUserExist = "SELECT COUNT(*) FROM users WHERE Discord_user_id=%s"
            cursor.execute(checkUserExist, (user.id,))
            userExists = cursor.fetchone()[0]

            if userExists == 0:
                insertUser = f"""
                INSERT INTO users (Discord_user_id, User_name)
                VALUES (%s, %s)
                """
                cursor.execute(insertUser, (user.id, user.name))
                connection.commit()
            for role in roles:
                print(role.id)
                emblemat_query = """
                    SELECT sheets.Sheet, roles.Role_name 
                    FROM sheets 
                    INNER JOIN roles ON sheets.Role_id = roles.RoleID 
                    WHERE roles.Discord_role_id = %s
                """
                cursor.execute(emblemat_query, (role.id,))
                results = cursor.fetchall()

                for i, result in enumerate(results, 1):
                    embed.add_field(name=f"{role.name} - Arkusz {i}", value=result[0], inline=False)
            
            if not embed.fields:
                embed.description = "Brak arkuszy do wyświetlenia."

            await interaction.response.send_message(embed=embed)
        except Error as e:
            print(f"Problem with the database! Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    @nextcord.slash_command(name='show_level', description="Zobacz swój aktualny level", guild_ids=[testServerId, serverId])
    async def myLevel(self, interaction: Interaction, role: nextcord.Role):
        try:
            connection = connectToDatabase()
            cursor = connection.cursor()
            user = interaction.user

            userLevelTable = """
                CREATE TABLE IF NOT EXISTS userLevel(
                    LevelID INT NOT NULL AUTO_INCREMENT,
                    User_id BIGINT NOT NULL,
                    Sheet_id INT NOT NULL,
                    Role_id BIGINT NOT NULL,
                    Unique_value BIGINT NOT NULL,
                    Status BOOLEAN,
                    PRIMARY KEY(LevelID),
                    UNIQUE (Unique_value)
                );
            """
            cursor.execute(userLevelTable)

            cursor.execute("SELECT UserID FROM users WHERE Discord_user_id = %s", (user.id,))
            user_id = cursor.fetchone()
            if not user_id:
                await interaction.response.send_message("Użytkownik nie istnieje w bazie danych.", ephemeral=True)
                return
            user_id = user_id[0]

            cursor.execute("SELECT RoleID FROM roles WHERE Discord_role_id = %s", (role.id,))
            role_id = cursor.fetchone()
            if not role_id:
                await interaction.response.send_message("Rola nie istnieje w bazie danych.", ephemeral=True)
                return
            role_id = role_id[0]

            cursor.execute("SELECT SheetID FROM sheets WHERE Role_id = %s", (role_id,))
            sheets = cursor.fetchall()
            if not sheets:
                await interaction.response.send_message("Nie ma arkusza dla tej roli.", ephemeral=True)
                return

            cursor.execute("SELECT Unique_value FROM userLevel")
            allUniqueValues = cursor.fetchall()
            allUniqueValues = [val[0] for val in allUniqueValues]

            for sheet in sheets:
                sheet_id = sheet[0]
                unique_value = int(user_id) + int(role_id) + int(sheet_id)
                if unique_value not in allUniqueValues:
                    addingToUserLevel = """
                        INSERT INTO userLevel (User_id, Sheet_id, Role_id, Unique_value, Status) 
                        VALUES (%s, %s, %s, %s, 0)
                    """
                    insertionInfo = (user_id, sheet_id, role_id, unique_value)
                    cursor.execute(addingToUserLevel, insertionInfo)
                    connection.commit()

            showLevel = """
                SELECT sheets.Sheet, userLevel.Status 
                FROM userLevel 
                INNER JOIN users ON users.UserID = userLevel.User_id 
                INNER JOIN sheets ON userLevel.Sheet_id = sheets.SheetID 
                INNER JOIN roles ON userLevel.Role_id = roles.RoleID 
                WHERE roles.RoleID = %s AND users.UserID = %s
            """
            cursor.execute(showLevel, (role_id, user_id))
            allQueries = cursor.fetchall()
            
            embed = nextcord.Embed(title=f"Twój level {user.name}", description=f"Jest to level dla ciebie i roli {role.name}", color=0x00ff00)
            for query in allQueries:
                embed.add_field(name=query[0], value=query[1], inline=True)
            await interaction.response.send_message(embed=embed)
        except Error as e:
            print(f"Problem with the database! Error: {e}")
        
        finally:
            if connection.is_connected():
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

def setup(client):
    client.add_cog(LevelSystem(client))
