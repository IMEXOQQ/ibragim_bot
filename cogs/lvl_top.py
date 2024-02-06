import nextcord
import asyncio
from settings import config
from database import sorted_list_users
from nextcord.ext import commands


class LvlTop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(send_messages=True)

    async def lvl_top(self, ctx, count = 1):
        
        guild_id = ctx.guild.id
        guild = ctx.guild
        
        row = await sorted_list_users(guild_id)

        emb = nextcord.Embed(title="Топ 10 по уровню:", color=0x992d22)

        for i in row[0:10]:
            emb.add_field(name=f"{count}. {guild.get_member(i[2])}: {i[3]}", value='', inline=False)

        await ctx.send(embed = emb)
        
def setup(bot):
    bot.add_cog(LvlTop(bot))
    print("COGS | Module Lvl_top successfully loaded")
    
