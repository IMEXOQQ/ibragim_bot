import nextcord
import asyncio
from database import add_user, get_user
from nextcord.ext import commands
from settings import config


class UserToDb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        if member.bot:
            return
        else:
            guild_id = message.guild.id
            user_id = message.author.id
            if await get_user(guild_id, user_id) == False:
                await add_user(guild_id, user_id)


def setup(bot):
    bot.add_cog(UserToDb(bot))
    print("COGS | Module User_to_db successfully loaded")
