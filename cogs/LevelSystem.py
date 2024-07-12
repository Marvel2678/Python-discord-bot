import mysql.connector
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from mysql.connector import Error
from main import serverId, testServerId
from connect import connectToDatabase
from matplotlib import pylab as plt
import os
class LevelSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name="show_emblemat", description="This command displays the user's sheets.", guild_ids=[testServerId, serverId])
    async def emblemat(self, interaction: Interaction):
        try:
            roles = interaction.user.roles
            embed = nextcord.Embed(
                title="Emblemat Arkuszy",
                description=f"Arkusze przypisane do użytkownika {interaction.user.mention}",
                color=nextcord.Color.blurple()
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)
            connection = connectToDatabase()
            cursor = connection.cursor()
            user = interaction.user
            checkUserExist = "SELECT COUNT(*) FROM users WHERE Discord_user_id=%s"
            cursor.execute(checkUserExist, (user.id,))
            userExists = cursor.fetchone()[0]

            if userExists == 0:
                insertUser = """
                INSERT INTO users (Discord_user_id, User_name)
                VALUES (%s, %s)
                """
                cursor.execute(insertUser, (user.id, user.name))
                connection.commit()

            for role in roles:
                emblemat_query = """
                    SELECT sheets.Sheet, sheets.SheetID
                    FROM sheets 
                    INNER JOIN roles ON sheets.Role_id = roles.RoleID 
                    WHERE roles.Discord_role_id = %s
                """
                cursor.execute(emblemat_query, (role.id,))
                results = cursor.fetchall()

                for i, result in enumerate(results, 1):
                    embed.add_field(
                        name=f"{role.name} - Arkusz {i}",
                        value=f"**Nazwa Arkusza:** {result[0]}\n**ID Arkusza:** {result[1]}",
                        inline=False
                    )

            if not embed.fields:
                embed.description = "Brak arkuszy do wyświetlenia."

            embed.set_footer(
                text="Matura Bot - Arkusze",
                icon_url=self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url
            )
            await interaction.response.send_message(embed=embed)
        except Error as e:
            print(f"Problem with the database! Error: {e}")
            await interaction.response.send_message("Wystąpił problem z bazą danych. Prosimy spróbować ponownie później.")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

                
    @nextcord.slash_command(name='show_done', description="Zobacz swój aktualny level", guild_ids=[testServerId, serverId])
    async def showDone(self, interaction: Interaction, role: nextcord.Role):
        try:
            connection = connectToDatabase()
            cursor = connection.cursor()
            user = interaction.user

            userLevelTable = """
                CREATE TABLE IF NOT EXISTS userDone(
                    UserDoneID INT NOT NULL AUTO_INCREMENT,
                    User_id BIGINT NOT NULL,
                    Sheet_id INT NOT NULL,
                    Role_id BIGINT NOT NULL,
                    Unique_value BIGINT NOT NULL,
                    Status BOOLEAN,
                    PRIMARY KEY(UserDoneID),
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

            cursor.execute("SELECT Unique_value FROM userDone")
            allUniqueValues = cursor.fetchall()
            allUniqueValues = [val[0] for val in allUniqueValues]
            for sheet in sheets:
                sheet_id = sheet[0]
                unique_value = str(user_id) + str(role_id) + str(sheet_id)
                if unique_value not in allUniqueValues:
                    addingToUserLevel = """
                        INSERT INTO userDone (User_id, Sheet_id, Role_id, Unique_value, Status) 
                        VALUES (%s, %s, %s, %s, 0)
                    """
                    insertionInfo = (user_id, sheet_id, role_id, unique_value)
                    cursor.execute(addingToUserLevel, insertionInfo)
                    connection.commit()

        except Error as e:
            print(f"Problem with the database! Error: {e}")
        
        finally:
            if connection.is_connected():
                showLevel = """
                    SELECT sheets.Sheet, userDone.Status 
                    FROM userDone 
                    INNER JOIN users ON users.UserID = userDone.User_id 
                    INNER JOIN sheets ON userDone.Sheet_id = sheets.SheetID 
                    INNER JOIN roles ON userDone.Role_id = roles.RoleID 
                    WHERE roles.RoleID = %s AND users.UserID = %s
                """
                cursor.execute(showLevel, (role_id, user_id))
                allQueries = cursor.fetchall()
                
                embed = nextcord.Embed(title=f"Twój level {user.name}", description=f"Jest to level dla ciebie i roli {role.name}", color=0x00ff00)
                for query in allQueries:
                    embed.add_field(name=query[0], value=query[1], inline=True)
                await interaction.response.send_message(embed=embed)
                if cursor:
                    cursor.close()
                if connection:
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
                    Role_id BIGINT NOT NULL,
                    Level INT NOT NULL,
                    HowManyDone INT NOT NULL,
                    Unique_key BIGINT NOT NULL,
                    PRIMARY KEY(LevelID),
                    UNIQUE (Unique_key)
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

            unique_key = int(str(user_id) + str(role_id))

            cursor.execute("SELECT COUNT(*) FROM userLevel WHERE Unique_key = %s", (unique_key,))
            unique_key_exists = cursor.fetchone()[0]

            if unique_key_exists == 0:
                addingToUserLevel = """
                    INSERT INTO userLevel (LevelID, User_id, Role_id, Level, HowManyDone, Unique_key) 
                    VALUES (NULL, %s, %s, 1, 0, %s)
                """
                insertionInfo = (user_id, role_id, unique_key)
                cursor.execute(addingToUserLevel, insertionInfo)
                connection.commit()

            cursor.execute("SELECT COUNT(*) FROM userDone WHERE User_id = %s AND Role_id = %s AND Status=1", (user_id,role_id))
            countDoneSheets = cursor.fetchone()[0]
            
            print(countDoneSheets)  
            
            #Updating info Level and HowManyDone
            
            print(int(countDoneSheets/5))
            
            #this is userLevel
            userLevel = 1 + int(countDoneSheets/5)
            
            #Level będzie się nabijał co 5 arkuszy dlatego razy 5
            
            howMuchTNextLevel = 5*(userLevel)
            
            UpdateLevel = """
                UPDATE userLevel SET Level = %s WHERE User_id = %s AND Role_id = %s;
            """
            cursor.execute(UpdateLevel, (userLevel, user_id, role_id))
            UpdateHowManyDone = """
                UPDATE userLevel SET HowManyDone = %s WHERE User_id = %s AND Role_id = %s;
            """
            cursor.execute(UpdateHowManyDone, (countDoneSheets, user_id, role_id))
            
            showLevel = """
                SELECT Level, HowManyDone 
                FROM userLevel 
                WHERE Role_id = %s AND User_id = %s
            """
            cursor.execute(showLevel, (role_id, user_id))
            result = cursor.fetchone()
            
             # Tworzenie wykresu
            # fig, ax = plt.subplots()
            # categories = ['Zrobione Arkusze', 'Pozostało do następnego poziomu']
            # values = [howMuchTNextLevel, howMuchTNextLevel - countDoneSheets]
            # ax.bar(categories, values, color=['#00ff00', '#ff0000'])
            # ax.set_ylabel('Ilość Arkuszy')
            # plt.title(f"Progres do kolejnego poziomu ({userLevel} -> {userLevel + 1})")

            # # Zapis wykresu
            # chart_path = f"./chart_img/progress_chart_{user.id}_{role.id}.png"
            # plt.savefig(chart_path)
            # plt.close()
            
            embed = nextcord.Embed(title=f"Masz {result[0]} Lvl!", description=f"Jest to level dla {user.mention} i roli **{role.name}**", color=0x00ff00)
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.add_field(name="Zrobione Arkusze", value=str(result[1]), inline=True)
            embed.add_field(name=f"Do {userLevel + 1} poziomu", value=f"{result[1]} / {howMuchTNextLevel}", inline=True)
            embed.set_footer(text="Matura Bot - Level System", icon_url=self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url)
            
            # file = nextcord.File(chart_path, filename="progress_chart.png")
            embed.set_image(url="attachment://progress_chart.png")

            await interaction.response.send_message(embed=embed)

            # Usunięcie lokalnego pliku wykresu
            # if os.path.exists(chart_path):
            #     os.remove(chart_path)
            
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
