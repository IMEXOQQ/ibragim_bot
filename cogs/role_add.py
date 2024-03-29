import nextcord
import asyncio
from settings import config
from database import add_role, get_role, get_role_only_one
from nextcord.ext import commands


class RoleAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)

    async def role_add(self, ctx, role:nextcord.Role = None):
        if role == None:
            await ctx.send(f"Вы не задали роль!!!")
            return
        guild_id = ctx.guild.id
        role_id = role.id
        if await get_role(guild_id, role_id):
            await ctx.send(f"<@&{role_id}> уже добавлен в БД!!!")
            return
        
        elif await get_role_only_one(guild_id):
            await ctx.send(f"Можно задавать, **только 1 роль**!!! удалите предыдущую, чтобы добавить новую.")
            return
        
        elif not await get_role(guild_id, role_id) and (not await get_role_only_one(guild_id)):
            await add_role(guild_id, role_id)
            await ctx.send(f"<@&{role_id}> добавлен в БД")
            return



def setup(bot):
    bot.add_cog(RoleAdd(bot))
    print("COGS | Module Role_add successfully loaded")
    
