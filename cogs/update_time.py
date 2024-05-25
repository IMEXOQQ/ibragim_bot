import nextcord
import asyncio
from settings import config
from database import time_set
from nextcord.ext import commands


class UpdateTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)

    async def update_time(self, ctx, hours:int=None):
        guild_id = ctx.author.guild.id
        await time_set(guild_id, hours)
        await ctx.send(f"Время обновления ролей {hours} hrs")


def setup(bot):
    bot.add_cog(UpdateTime(bot))
    print("COGS | Module Update_time successfully loaded")
    
