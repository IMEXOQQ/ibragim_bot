import nextcord
import asyncio
from settings import config
from database import add_role, get_role, get_role_only_one
from nextcord import Interaction, SlashOption
from nextcord.ext import commands


class RoleAddSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(description="Добавить роль в БД")
    @commands.has_permissions(administrator=True)
    async def role_add(self, ctx, role:nextcord.Role = SlashOption(description="Роль", required=True)):
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
    bot.add_cog(RoleAddSlash(bot))
    print("COGS | Module Role_add_slash successfully loaded")
    
