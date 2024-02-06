import nextcord
import asyncio
from settings import config
from database import get_lvl, get_user, add_user
from nextcord.ext import commands


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(send_messages=True)

    async def info(self, ctx, member:nextcord.Member = None):
        if member == None:
            member = ctx.author
        elif member.bot:
            await ctx.send("Ничего интересного...")
            return
        
        user_id = member.id
        guild_id = member.guild.id
        
        row = await get_lvl(guild_id, user_id)
        if row != None:
            lvl = row[0]
            xp = row[1]
            likes = row[2]
            
            emb = nextcord.Embed(title="Информация о пользователе", color=member.color)
            emb.add_field(name="Имя:", value=member.display_name,inline=False)
            
            status = member.status
            if status == nextcord.Status.online:
                temp = " В сети"
            elif status == nextcord.Status.offline:
                temp = " Не в сети"
            if status == nextcord.Status.idle:
                temp = " Не активен"
            if status == nextcord.Status.dnd:
                temp = " Не беспокоить"

            emb.add_field(name="Активность:", value=temp,inline=False)
            emb.add_field(name="Лайки:", value=f"{likes}",inline=False)
            emb.add_field(name="Уровень:", value=lvl,inline=False)
            emb.add_field(name="Опыт:", value=f"{xp} / {100*(lvl+1)*lvl}",inline=False)
            emb.set_thumbnail(url=member.avatar)
            await ctx.send(embed = emb)
        else:
            return

def setup(bot):
    bot.add_cog(UserInfo(bot))
    print("COGS | Module User_info successfully loaded")
    
