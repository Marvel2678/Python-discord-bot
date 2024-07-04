import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
from main import serverId
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
            
    @nextcord.slash_command(name="clear", description="Usuń wiadomości z kanału", guild_ids=[serverId])
    async def clear(self, interaction: Interaction, amount: int):
        # Sprawdzenie uprawnień użytkownika
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Nie masz uprawnień do usuwania wiadomości.", ephemeral=True)
            return

        await interaction.response.defer()  # Opóźnienie odpowiedzi, aby zapobiec przekroczeniu czasu

        # Usuwanie wiadomości
        deleted = await interaction.channel.purge(limit=amount)
        
        await interaction.followup.send(f"Usunięto {len(deleted)} wiadomości.", ephemeral=True)
async def setup(client):
    client.add_cog(Moderator(client))
