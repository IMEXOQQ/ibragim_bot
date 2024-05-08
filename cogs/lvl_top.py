import nextcord
import asyncio
from settings import config
from database import sorted_list_users
from nextcord.ext import commands


class LvlTopSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(description="Топ 10 по уровню")
    @commands.has_permissions(send_messages=True)

    async def lvl_top(self, ctx):
        
        guild_id = ctx.guild.id
        guild = ctx.guild
        
        row = await sorted_list_users(guild_id)

        emb = nextcord.Embed(title="Топ 10 по уровню:", color=0x992d22)

        count = 1
        for i in row[0:10]:
            emb.add_field(name=f"{count}. {guild.get_member(i[2])}: {i[3]}", value='', inline=False)
            count += 1

        await ctx.send(embed = emb)
        
def setup(bot):
    bot.add_cog(LvlTopSlash(bot))
    print("COGS | Module Lvl_top successfully loaded")
    
