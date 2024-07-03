import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
class Moderator(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"User {member.name} has been kicked! Reason: {reason}")
        except Exception as e:
            await ctx.send(f"Failed to kick {member.name}: {e}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to kick people!")
        else:
            await ctx.send(f"An error occurred: {error}")

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"User {member.name} has been banned! Reason: {reason}")
        except Exception as e:
            await ctx.send(f"Failed to ban {member.name}: {e}")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to ban people!")
        else:
            await ctx.send(f"An error occurred: {error}")

async def setup(client):
    client.add_cog(Moderator(client))
