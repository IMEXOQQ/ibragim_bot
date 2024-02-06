import nextcord
import asyncio
from database import expierence, get_user, add_user, get_lvl
from nextcord.ext import commands
from settings import config


class UserExpierence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    #Expierence to user
    async def on_message(self, message):
        guild_id = message.guild.id
        user_id = message.author.id
        content = message.content
        if await get_user(guild_id, user_id):
            if await expierence(guild_id, user_id, content):
                await message.channel.send(f"<@{user_id}> новый уровень!")

def setup(bot):
    bot.add_cog(UserExpierence(bot))
    print("COGS | Module User_expierence successfully loaded")
