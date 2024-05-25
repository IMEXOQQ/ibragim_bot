import nextcord
import asyncio
from settings import config
from database import delete_channel, get_channel
from nextcord import Interaction, SlashOption
from nextcord.ext import commands


class ChannelDeleteSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Удаление канала из системы лайков")
    @commands.has_permissions(administrator=True)

    async def channel_delete(self, ctx, channel:nextcord.TextChannel = SlashOption(description="Канал", required= True)):
        channel_id = channel.id
        guild_id = ctx.guild.id
        if await get_channel(guild_id, channel_id):
            await delete_channel(channel_id)
            await ctx.send(f"<#{channel_id}> канал был удалён из БД")
        elif not await get_channel(guild_id, channel_id):
            await ctx.send(f"<#{channel_id}> канал не был добавлен в БД!!!")

def setup(bot):
    bot.add_cog(ChannelDeleteSlash(bot))
    print("COGS | Module Channel_delete_slash successfully loaded")
    
