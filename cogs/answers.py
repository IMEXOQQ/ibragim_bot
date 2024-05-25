import nextcord
import asyncio
from settings import config
from nextcord.ext import commands
'''реакция на маты/похвалу в сторону бота что-то ничего не придумал...'''


class Answers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_message(self, ctx, error):
        print(error)
        await ctx.send("")



def setup(bot):
    bot.add_cog(Answers(bot))
    print("COGS | Module Answers successfully loaded")
    
