import nextcord
import asyncio
from settings import config
from database import reset_lvl
from nextcord.ext import commands


class ResetLvlSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(description="Обнуление уровней")
    @commands.has_permissions(administrator=True)

    async def reset_lvl(self, ctx):
        guild_id = ctx.guild.id
        await reset_lvl(guild_id)
        await ctx.send(f"Уровни были обнулены")



def setup(bot):
    bot.add_cog(ResetLvlSlash(bot))
    print("COGS | Module Reset_lvl_slash successfully loaded")
    
