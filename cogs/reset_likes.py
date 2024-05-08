import nextcord
import asyncio
from settings import config
from database import reset_likes
from nextcord.ext import commands


class ResetLikeSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Обнуление лайков")
    @commands.has_permissions(administrator=True)

    async def reset_likes(self, ctx):
        guild_id = ctx.guild.id
        await reset_likes(guild_id)
        await ctx.send(f"Лайки были обнулены")



def setup(bot):
    bot.add_cog(ResetLikeSlash(bot))
    print("COGS | Module Reset_like_slash successfully loaded")
    
