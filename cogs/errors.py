import nextcord
import asyncio
from settings import config
from nextcord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        await ctx.send("Таких команд я не знаю.")



def setup(bot):
    bot.add_cog(Errors(bot))
    print("COGS | Module Errors successfully loaded")
    
