import nextcord
from nextcord.ext import commands
import nextcord
from nextcord.utils import get
from nextcord.ext.commands import has_permissions, MissingPermissions
def printingAllCommands(command_list: dict):
    result = ""
    index = 0
    for key, value in command_list.items():
        index += 1
        result += f"{index}. **{key}**: {value}\n"
    return result

class UserCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def commandsCommand(self, ctx):
        listModerator = {
            "kick": "Its kicking other member from this server",
            "ban": "Its banning member",
        }
        listUser = {
            "hello": "this is hello command",
        }
        listTesting = {
            "embed": "Testing command"
        }
        moderatorCommands = printingAllCommands(listModerator)
        userCommandsStr = printingAllCommands(listUser)
        testCommands = printingAllCommands(listTesting)
        
        embed = nextcord.Embed(title='Moje Komendy!', description='To jest moja lista komend: \n')
        embed.add_field(name="**Moderator**", value=f"{moderatorCommands}", inline=False)
        embed.add_field(name="**User**", value=f"{userCommandsStr}", inline=False)
        embed.add_field(name="**Testing**", value=f"{testCommands}", inline=False)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def embed(self, ctx):
        embed = nextcord.Embed(title="First embed", color=0xFF5733, description="test embed")
        embed.set_author(name="Marcel", icon_url="https://cdn-icons-png.flaticon.com/512/25/25231.png", url="https://www.facebook.com/profile.php?id=100012886985945")
        embed.set_thumbnail(url="https://imgs.search.brave.com/q4s8VRrvb_RKhnw6-Vic5PhLGPqUG182-UMObxh1lCw/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTQ4/NjkwNzI5Mi9waG90/by9tYW4tY2xpbWJp/bmctdXAtbW91bnRh/aW4tY2xpZmYtZG9y/a2luZy1oYXJkLXRv/LXJlYWNoLWdvYWxz/LndlYnA_Yj0xJnM9/MTcwNjY3YSZ3PTAm/az0yMCZjPUxpM1V0/bG03QmhIbVFheGg2/QlhMbDNrNUVLaDR6/RlFFZ2laZS1uc1Bw/TDA9")
        embed.set_footer(text="All the best to you! Administrators")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addRole(self, ctx, user: nextcord.Member, *, role: nextcord.Role):
        if role in user.roles:
            await ctx.send(f"User {user.name} already has this role!")
        else:
            await user.add_roles(role)
            await ctx.send(f"User {user.name} has new role {role.name}!")

    @addRole.error
    async def addRole_error(self, ctx, error):
        bot_member = ctx.guild.me
        bot_permissions = ctx.channel.permissions_for(bot_member)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid user or role.")
        elif bot_permissions.manage_roles:
            await ctx.send("I don't have permission to manage this role.")
            return
        else:
            await ctx.send("An error occurred.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removeRole(self, ctx, user: nextcord.Member, *, role: nextcord.Role):
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.send(f"User {user.name} has deleted role {role.name}!")
        else:
            await ctx.send(f"User {user.name} doesn't have this role!")

    @removeRole.error
    async def removeRole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid user or role.")
        else:
            await ctx.send("An error occurred.")       
        
async def setup(client):
    client.add_cog(UserCommands(client))
    
