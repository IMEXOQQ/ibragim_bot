import nextcord
import asyncio
from settings import config
from database import reset_lvl
from nextcord.ext import commands


class ResetLvl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)

    async def reset_lvl(self, ctx):
        guild_id = ctx.guild.id
        await reset_lvl(guild_id)
        await ctx.send(f"Уровни были обнулены")



def setup(bot):
    bot.add_cog(ResetLvl(bot))
    print("COGS | Module Reset_lvl successfully loaded")
    
