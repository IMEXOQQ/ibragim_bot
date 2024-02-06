import nextcord
import asyncio
from database import plus_like, minus_like
from nextcord.ext import commands
from settings import config


class LikeCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        channel_id = event.channel_id
        guild_id = event.guild_id
        message_id = event.message_id
        guild = self.bot.get_guild(guild_id)
        member = event.member

        channel = guild.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        author = message.author
        author_id = author.id

        emoji = event.emoji.name
        if emoji == '❤️':
            if (not member.bot) and (not author.bot) and (author != member):
                await plus_like(guild_id, author_id)
        else: return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event):
        channel_id = event.channel_id
        guild_id = event.guild_id
        message_id = event.message_id
        guild = self.bot.get_guild(guild_id)
        member = nextcord.utils.get(guild.members, id=event.user_id)

        channel = guild.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        author = message.author
        author_id = author.id

        emoji = event.emoji.name
        if emoji == '❤️':
            if (not member.bot) and (not author.bot) and member != author:
                await minus_like(guild_id, author_id)

def setup(bot):
    bot.add_cog(LikeCount(bot))
    print("COGS | Module Like_count successfully loaded")
