import nextcord
import asyncio
from settings import config
from database import delete_role, get_role
from nextcord.ext import commands


class RoleDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)

    async def role_delete(self, ctx, role_id:int=None):
        guild_id = ctx.guild.id
        if await get_role(guild_id, role_id):
            await delete_role(role_id)
            await ctx.send(f"<@&{role_id}> роль была удалена из БД")
        elif not await get_role(guild_id, role_id):
            await ctx.send(f"<@&{role_id}> роль не была добавлена в БД!!!")

def setup(bot):
    bot.add_cog(RoleDelete(bot))
    print("COGS | Module Role_delete successfully loaded")
    
