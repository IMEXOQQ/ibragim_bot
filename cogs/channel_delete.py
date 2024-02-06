import nextcord
import asyncio
from settings import config
from database import delete_channel, get_channel
from nextcord.ext import commands


class ChannelDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)

    async def channel_delete(self, ctx, channel_id:int=None):
        guild_id = ctx.guild.id
        if await get_channel(guild_id, channel_id):
            await delete_channel(channel_id)
            await ctx.send(f"<#{channel_id}> канал был удалён из БД")
        elif not await get_channel(guild_id, channel_id):
            await ctx.send(f"<#{channel_id}> канал не был добавлен в БД!!!")

def setup(bot):
    bot.add_cog(ChannelDelete(bot))
    print("COGS | Module Channel_delete successfully loaded")
    
