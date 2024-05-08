import nextcord
import asyncio
from settings import config
from database import delete_blocked_channel, get_blocked_channel
from nextcord import Interaction, SlashOption
from nextcord.ext import commands


class UnblockChannelSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Разблокировка канала для получения опыта")
    @commands.has_permissions(administrator=True)

    async def unblock_channel(self, ctx, channel:nextcord.TextChannel = SlashOption(description="Канал", required= True)):
        channel_id = channel.id
        guild_id = ctx.guild.id
        if await get_blocked_channel(guild_id, channel_id):
            await delete_blocked_channel(channel_id)
            await ctx.send(f"<#{channel_id}> канал был разблокирован для опыта")
        elif not await get_blocked_channel(guild_id, channel_id):
            await ctx.send(f"<#{channel_id}> канал не был заблокирован для опыта!!!")

def setup(bot):
    bot.add_cog(UnblockChannelSlash(bot))
    print("COGS | Module Unblock_Channel_slash successfully loaded")
    
