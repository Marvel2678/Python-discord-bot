import nextcord
from nextcord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if "old spice" in message.content: 
            await message.channel.send("Did someone say old spice?")
            embed = nextcord.Embed(title='')
            embed.set_image(url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnJ3Yno2bmZmNGN1NWlxNzRicjAyNmc4NXZhMHh1dzVueXM3eWp5ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zrcH6qNGE4rG8/giphy.gif")
            await message.channel.send(embed = embed)
            
    # @commands.command()
    # async def memy(self, ctx):
        
        
def setup(client):
    client.add_cog(Fun(client))