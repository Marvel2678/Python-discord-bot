import datetime
import requests
import nextcord
from nextcord.ext import commands, tasks
import aioschedule as schedule
import asyncio
import pytz
from datetime import datetime
from html.parser import HTMLParser
from main import serverId, testServerId

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return ''.join(self.text)
    
    
class DailyChallenge(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_task.start()

    @nextcord.slash_command(name="daily", description="Fetch today's LeetCode daily challenge.", guild_ids=[serverId, testServerId])
    async def get_leetcode_daily_challenge(self, interaction: nextcord.Interaction):
        url = 'https://leetcode.com/graphql'
        query = '''
        {
            activeDailyCodingChallengeQuestion {
                link
                question {
                    title
                    content
                    difficulty
                }
            }
        }
        '''
        response = requests.post(url, json={'query': query})
        data = response.json()

        if 'errors' in data:
            await interaction.response.send_message("Failed to fetch the daily challenge.")
            return

        daily_challenge = data['data']['activeDailyCodingChallengeQuestion']
        title = daily_challenge['question']['title']
        content = daily_challenge['question']['content']
        difficulty = daily_challenge['question']['difficulty']
        link = 'https://leetcode.com' + daily_challenge['link']
        
        parser = HTMLTextExtractor()
        parser.feed(content)
        content_text = parser.get_text()
        
        embed_en = nextcord.Embed(title="LeetCode Daily Challenge", color=0x00ff00)
        embed_en.add_field(name="Title", value=title, inline=False)
        embed_en.add_field(name="Difficulty", value=difficulty, inline=False)
        embed_en.add_field(name="Description", value=content_text[:1024], inline=False)
        embed_en.add_field(name="Link", value=link, inline=False)

        # responses_pl = [
        #     f"Dzisiejsze wyzwanie to: {title}\nMożesz je znaleźć tutaj: {link}",
        #     f"Oto twoje codzienne wyzwanie programistyczne: {title}\nSprawdź to: {link}",
        #     f"Gotowy na dzisiejsze wyzwanie? Nazywa się {title}\nLink: {link}"
        # ]

        # if language == "en":
        # else:
        #     response = random.choice(responses_pl)

        await interaction.response.send_message(embed=embed_en)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.client.user}')
    async def daily_event(self):
        print("Running daily_event")  # Debug log
        channel = self.client.get_channel(1260951026580852738)  # Upewnij się, że masz poprawny ID kanału
        if channel is None:
            print("Channel not found!")  # Debug log
            return
        url = 'https://leetcode.com/graphql'
        query = '''
        {
            activeDailyCodingChallengeQuestion {
                link
                question {
                    title
                    content
                    difficulty
                }
            }
        }
        '''
        response = requests.post(url, json={'query': query})
        data = response.json()

        if 'errors' in data:
            await channel.send("Failed to fetch the daily challenge.")
            return

        daily_challenge = data['data']['activeDailyCodingChallengeQuestion']
        title = daily_challenge['question']['title']
        content = daily_challenge['question']['content']
        difficulty = daily_challenge['question']['difficulty']
        link = 'https://leetcode.com' + daily_challenge['link']

        parser = HTMLTextExtractor()
        parser.feed(content)
        content_text = parser.get_text()

        embed_en = nextcord.Embed(title="LeetCode Daily Challenge", color=0x00ff00)
        embed_en.add_field(name="Title", value=title, inline=False)
        embed_en.add_field(name="Difficulty", value=difficulty, inline=False)
        embed_en.add_field(name="Description", value=content_text[:1024], inline=False)
        embed_en.add_field(name="Link", value=link, inline=False)

        await channel.send(embed=embed_en)
        
    def get_local_time(self, timezone):
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        local_time = utc_now.astimezone(pytz.timezone(timezone))
        return local_time.strftime("%H:%M")
    
    @tasks.loop(seconds=60)
    async def daily_task(self):
        current_time = self.get_local_time("Europe/Warsaw")
        print(f"Current time: {current_time}")  # Debug log
        if current_time == "09:00":
            await self.daily_event()

    @daily_task.before_loop
    async def before_daily_task(self):
        print("Triggering daily_event")  # Debug log
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(DailyChallenge(client))