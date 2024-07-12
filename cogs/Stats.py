import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import matplotlib.pyplot as plt
from main import serverId, testServerId
from connect import connectToDatabase

class StatsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="chart", description="Generates a pie chart", guild_ids=[testServerId, serverId])
    async def piechart(self, interaction: Interaction):
        user = interaction.user
        
        connection = connectToDatabase()
        cursor = connection.cursor()
        selectUserID = "SELECT UserID FROM users WHERE Discord_user_id = %s"
        cursor.execute(selectUserID, (user.id,))
        userID = cursor.fetchone()[0]
        
        countAllSheets = "SELECT COUNT(*) FROM userLevel WHERE User_id = %s"
        cursor.execute(countAllSheets, (userID,))
        countAllSheetsForUser = cursor.fetchone()[0]
        
        countDoneSheets = "SELECT COUNT(*) FROM userLevel WHERE User_id = %s AND Status = 1"
        cursor.execute(countDoneSheets, (userID,))
        countDoneSheetsForUser = cursor.fetchone()[0]
        print(f"countAllSheetsForUser: {countAllSheetsForUser}")
        print(f"countDoneSheetsForUser: {countDoneSheetsForUser}")
        #Information to chart
        labels = 'Zrobione', 'Nie zrobione'
        sizes = [countDoneSheetsForUser, (countAllSheetsForUser - countDoneSheetsForUser)]
        colors = ['green', 'red']
        explode = (0.1, 0)  # explode 1st slice

        # Plot
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the plot
        plt.savefig('./chart_img/pie_chart.png')
        plt.close()

        # Send the plot
        with open('pie_chart.png', 'rb') as file:
            await interaction.response.send_message(file=nextcord.File(file, 'pie_chart.png'))

def setup(client):
    client.add_cog(StatsCog(client))