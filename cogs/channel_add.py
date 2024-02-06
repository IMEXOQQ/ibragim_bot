import nextcord
import asyncio
from settings import config
from database import add_channel, get_channel
from nextcord.ext import commands


class ChannelAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)

    async def channel_add(self, ctx, channel_id:int=None):
        guild_id = ctx.guild.id
        if await get_channel(guild_id, channel_id):
            await ctx.send(f"<#{channel_id}> уже добавлен в БД!!!")
        elif not await get_channel(guild_id, channel_id):
            await add_channel(guild_id, channel_id)
            await ctx.send(f"<#{channel_id}> добавлен в БД")

def setup(bot):
    bot.add_cog(ChannelAdd(bot))
    print("COGS | Module Channel_add successfully loaded")
    
