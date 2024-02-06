import nextcord
import asyncio
from settings import config
from database import reset_likes
from nextcord.ext import commands


class ResetLike(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)

    async def reset_likes(self, ctx):
        guild_id = ctx.guild.id
        await reset_likes(guild_id)
        await ctx.send(f"Лайки были обнулены")



def setup(bot):
    bot.add_cog(ResetLike(bot))
    print("COGS | Module Reset_like successfully loaded")
    
