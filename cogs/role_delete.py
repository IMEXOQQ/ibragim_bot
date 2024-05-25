import nextcord
import asyncio
from settings import config
from database import delete_role, get_role
from nextcord import Interaction, SlashOption
from nextcord.ext import commands


class RoleDeleteSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @nextcord.slash_command(description="Удалить роль из БД")
    @commands.has_permissions(administrator=True)

    async def role_delete(self, ctx, role:nextcord.Role = SlashOption(description="Роль", required=True)):
        guild_id = ctx.guild.id
        role_id = role.id
        if await get_role(guild_id, role_id):
            await delete_role(role_id)
            await ctx.send(f"<@&{role_id}> роль была удалена из БД")
        elif not await get_role(guild_id, role_id):
            await ctx.send(f"<@&{role_id}> роль не была добавлена в БД!!!")

def setup(bot):
    bot.add_cog(RoleDeleteSlash(bot))
    print("COGS | Module Role_delete_slash successfully loaded")
    
