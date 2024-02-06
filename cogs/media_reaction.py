import nextcord
import asyncio
from database import get_channel
from nextcord.ext import commands
from settings import config


class MediaReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id = message.guild.id
        channel_id = message.channel.id
        if await get_channel(guild_id, channel_id):
            if message.attachments:
                emoji = '❤️'
                await message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(MediaReaction(bot))
    print("COGS | Module Media_reaction successfully loaded")
