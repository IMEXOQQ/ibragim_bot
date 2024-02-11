import nextcord
import asyncio
from settings import config
from database import get_lvl
from nextcord.ext import commands


class HelpSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(send_messages=True)

    async def help(self, ctx):
        embed = nextcord.Embed(title="Информация по боту", colour=0x33d17a)

        embed.add_field(name="Команды для пользователей:",
                        value="**%help** - информация по боту.\n**%info** - информация о участниках.\n**%lvl_top** - топ 10 по уровню.\n**%like_top** - топ 10 по уровню.",
                        inline=False)
        embed.add_field(name="Команды для администрации:",
                        value="**%channel_add** - добавить канал для реакций медиаконтента.\n**%channel_remove** - убрать канал.\n**%role_add**  - добавить роль для выдачи (__только 1 роль!!!__).\n**%role_delete**- удалить роль.\n**%reset_lvl** - обнулить уровни.\n**%reset_likes** - обнулить лайки.",
                        inline=False)
        embed.add_field(name="Особенности:",
                        value="🔴 Уровни и опыт за кол-во сообщений.\n\n🔴 Система лайков пользователей и медиаконтента.\nПользователи смогут 'лайкать' медиаконтент и 'кидать лайки' через реакцию ❤️\n\n🔴 Автообновление ролей каждые 3 дня.\nТоп 5 пользователей по уровню получают особенную роль. Выдача ролей осуществляется автоматически",
                        inline=False)
        embed.add_field(name="Создатель бота:",
                        value="**IMEXO**\nБольшую помощь оказал **[Fanyatsu](https://fanyat.su/)**",
                        inline=False)

        embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5696-cypher.png")

        embed.set_footer(text="По всем вопросам и проблемам обращаться к IMEXO")

        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(HelpSlash(bot))
    print("COGS | Module Help_slash successfully loaded")
    
