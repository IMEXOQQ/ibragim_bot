import nextcord
import asyncio
from database import delete_user, get_user
from nextcord.ext import commands
from settings import config


class UserLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_leave(member):
        guild_id = member.guild.id
        user_id = member.id
        if get_user(guild_id, user_id):
            delete_user(guild_id, user_id)
        else: return


def setup(bot):
    bot.add_cog(UserLeave(bot))
    print("COGS | Module User_Leave successfully loaded")
