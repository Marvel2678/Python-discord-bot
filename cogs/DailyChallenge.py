import requests
import nextcord
from nextcord.ext import commands, tasks
import aioschedule as schedule
import asyncio
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
    async def daily_event(self):
        channel = self.client.get_channel(1260951026580852738)
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

    @tasks.loop(seconds=60)  # This loop runs every 60 seconds
    async def daily_task(self):
        current_time = nextcord.utils.utcnow().strftime("%H:%M")
        if current_time == "14:30":
            await self.daily_event()

    @daily_task.before_loop
    async def before_daily_task(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(DailyChallenge(client))