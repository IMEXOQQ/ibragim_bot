import nextcord
import asyncio
from database import expierence, get_user, add_user
from nextcord.ext import commands, tasks
from settings import config


class VoiceExpierence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_experience.start()

    @tasks.loop(minutes=10)
    async def update_experience(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.voice and member.voice.channel:
                    if not await get_user(member.guild.id, member.id):
                        await add_user(member.guild.id, member.id)
                        return
                    content = "1"*20
                    if await expierence(member.guild.id, member.id, content):
                        await member.voice.channel.send(f"<@{member.id}> новый уровень!")

    @update_experience.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()



def setup(bot):
    bot.add_cog(VoiceExpierence(bot))
    print("COGS | Module Voice_Experience successfully loaded")
