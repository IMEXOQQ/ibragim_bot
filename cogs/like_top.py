import nextcord
import asyncio
from settings import config
from database import sorted_list_users_like
from nextcord.ext import commands


class LikeTopSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(description="Топ 10 по лайкам")
    @commands.has_permissions(send_messages=True)

    async def like_top(self, ctx):
        
        guild_id = ctx.guild.id
        guild = ctx.guild
        
        row = await sorted_list_users_like(guild_id)

        emb = nextcord.Embed(title="Топ 10 по лайкам:", color=0x992d22)

        count = 1
        for i in row[0:10]:
            emb.add_field(name=f"{count}. {guild.get_member(i[2])}: {i[5]}", value='', inline=False)
            count+=1


        await ctx.send(embed = emb)
        
def setup(bot):
    bot.add_cog(LikeTopSlash(bot))
    print("COGS | Module Like_top_slash successfully loaded")
    
