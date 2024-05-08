import nextcord
import asyncio
from settings import config
from database import add_channel, get_channel
from nextcord import Interaction, SlashOption
from nextcord.ext import commands


class ChannelAddSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(description="Добавление канала в систему лайков")
    @commands.has_permissions(administrator=True)

    async def channel_add(self, ctx, channel:nextcord.TextChannel = SlashOption(description="Канал", required= True)):
        channel_id = channel.id
        guild_id = ctx.guild.id
        if await get_channel(guild_id, channel_id):
            await ctx.send(f"<#{channel_id}> уже добавлен в БД!!!")
        elif not await get_channel(guild_id, channel_id):
            await add_channel(guild_id, channel_id)
            await ctx.send(f"<#{channel_id}> добавлен в БД")

def setup(bot):
    bot.add_cog(ChannelAddSlash(bot))
    print("COGS | Module Channel_add_slash successfully loaded")
    
