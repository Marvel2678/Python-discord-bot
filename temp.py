import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
mainColor = 0xFF5733
defaultImg = "https://cdn-icons-png.flaticon.com/512/25/25231.png"
botName = 'MaturaBot'
listModerator = {
    # "hello": "this is hello command",
    "kick": "Its kicking other member from this server",
    "ban": "Its banning member",
    # "embed": "Testing command"
}
listUser = {
    "hello": "this is hello command",
}
listTesting = {
    "embed": "Testing command"
}
client = commands.Bot(command_prefix='!', intents=intents)

def EmbedBuilder(title, description, color, name, icon_url, url:None):
    embed = discord.Embed(title=title, color=color, description=description, url=url)
    embed.set_author(name=name, icon_url=icon_url)
    embed.set_footer(text="All the best to you! Administrators")
    return embed

def printingAllCommands(list: dict):
    command_list = ""
    index = 0
    for key, value in list.items():
        index +=1
        command_list += f"{index}. **{key}**: {value}\n"
    return command_list
# def setField(name, value):
    
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="twoich komend"))
    print("The bot is active now!")
@client.command()
async def hello(ctx):
    await ctx.send("Hello! I hope you have a good day!")
@client.command()
async def commands(ctx):
    # await ctx.send('Hello, I am the first python bot!')
    moderatorCommands = printingAllCommands(listModerator)
    userCommands = printingAllCommands(listUser)
    testCommands = printingAllCommands(listTesting)
    embed = discord.Embed(title='Moje Komendy!', description=f'To jest moja lista komend: \n', color=mainColor)
    embed.add_field(name="**Moderator**", value=f"{moderatorCommands}", inline=False)
    embed.add_field(name="**User**", value=f"{userCommands}", inline=False)
    embed.add_field(name="**Testing**", value=f"{testCommands}", inline=False)
    await ctx.send(embed = embed)
@client.event
async def on_member_join(member):
    channel = client.get_channel(1141086688706306088)
    if channel:
        await channel.send(f"Hello {member.name}! Welcome to the server!")
    else:
        print("Channel not found or bot lacks permission to access the channel.")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1141296683821576232)
    if channel:
        await channel.send(f"Goodbye {member.name} :(. We hope you come back to us soon!")
    else:
        print("Channel not found or bot lacks permission to access the channel.")

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"User {member.name} has been kicked! Reason: {reason}")
    except Exception as e:
        await ctx.send(f"Failed to kick {member.name}: {e}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to kick people!")
    else:
        await ctx.send(f"An error occurred: {error}")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"User {member.name} has been banned! Reason: {reason}")
    except Exception as e:
        await ctx.send(f"Failed to ban {member.name}: {e}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to ban people!")
    else:
        await ctx.send(f"An error occurred: {error}")

@client.command()
async def embed(ctx):
    embed = discord.Embed(title="First embed", color=0xFF5733, description="test embed")
    embed.set_author(name="Marcel", icon_url="https://cdn-icons-png.flaticon.com/512/25/25231.png", url="https://www.facebook.com/profile.php?id=100012886985945")
    embed.set_thumbnail(url="https://imgs.search.brave.com/q4s8VRrvb_RKhnw6-Vic5PhLGPqUG182-UMObxh1lCw/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTQ4/NjkwNzI5Mi9waG90/by9tYW4tY2xpbWJp/bmctdXAtbW91bnRh/aW4tY2xpZmYtd29y/a2luZy1oYXJkLXRv/LXJlYWNoLWdvYWxz/LndlYnA_Yj0xJnM9/MTcwNjY3YSZ3PTAm/az0yMCZjPUxpM1V0/bG03QmhIbVFheGg2/QlhMbDNrNUVLaDR6/RlFFZ2laZS1uc1Bw/TDA9")
    embed.set_footer(text="All the best to you! Administrators")
    await ctx.send(embed=embed)
    
@client.command()
async def message(ctx, user: discord.member, *, message: None):
    message = "Witaj! Jako domyślny bot tego serwera życzę ci miłej pracy wśród nas nad maturą."
    await ctx.send(embed = EmbedBuilder(title="Witaj na serwerze!", description=message, name="Powodzenia! Administratorzy bota i serwera!"))

client.run("MTI1MzQzMTY5MTA1ODM0ODAzMg.GZlEBE.NwjV4vx5_0wHgVEYf8rsQLWlIOrdGchLSe67Ks")
