import nextcord
import asyncio
from settings import config
from database import add_blocked_channel, get_blocked_channel
from nextcord import Interaction, SlashOption
from nextcord.ext import commands


class BlockChannelSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(description="Блокировка канала от получения опыта")
    @commands.has_permissions(administrator=True)

    async def block_channel(self, ctx, channel:nextcord.TextChannel = SlashOption(description="Канал", required= True)):
        channel_id = channel.id
        guild_id = ctx.guild.id
        if await get_blocked_channel(guild_id, channel_id):
            await ctx.send(f"<#{channel_id}> уже заблокирован для опыта!!!")
        elif not await get_blocked_channel(guild_id, channel_id):
            await add_blocked_channel(guild_id, channel_id)
            await ctx.send(f"<#{channel_id}> заблокирован для опыта")

def setup(bot):
    bot.add_cog(BlockChannelSlash(bot))
    print("COGS | Module Block_Channel_slash successfully loaded")
    
