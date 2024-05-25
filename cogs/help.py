import nextcord
import asyncio
from settings import config
from database import get_lvl
from nextcord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Помощь по боту")
    @commands.has_permissions(send_messages=True)

    async def help(self, ctx):
        embed = nextcord.Embed(title="Информация по боту", colour=0x33d17a)

        embed.add_field(name="Команды для пользователей:",
                        value="**%help** - информация по боту.\n**%info** - информация о участниках.\n**%lvl_top** - топ 10 по уровню.\n**%like_top** - топ 10 по уровню.\n**%profile** - получение информации об участниках картинкой.",
                        inline=False)
        embed.add_field(name="Команды для администрации:",
                        value="**%channel_add** - добавить канал для реакций медиаконтента.\n**%channel_remove** - убрать канал.\n**%role_add**  - добавить роль для выдачи (__только 1 роль!!!__).\n**%role_delete**- удалить роль.\n**%reset_lvl** - обнулить уровни.\n**%reset_likes** - обнулить лайки.\n**%block_channel** - заблокировать канал для получения опыта.\n**%unblock_channel** - разблокировать канал для получения опыта.",
                        inline=False)
        embed.add_field(name="Особенности:",
                        value="🔴 Уровни и опыт за кол-во сообщений и время пребывания в голосовом канале.\n\n🔴 Система лайков пользователей и медиаконтента.\nПользователи смогут 'лайкать' медиаконтент и 'кидать лайки' через реакцию ❤️\n\n🔴 Автообновление ролей каждые 3 дня.\nТоп 5 пользователей по уровню получают особенную роль. Выдача ролей осуществляется автоматически",
                        inline=False)
        embed.add_field(name="Создатель бота:",
                        value="**IMEXO**\nБольшую помощь оказал **[Fanyatsu](https://fanyat.su/)**",
                        inline=False)

        embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5696-cypher.png")

        embed.set_footer(text="По всем вопросам и проблемам обращаться к IMEXO")

        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Help(bot))
    print("COGS | Module Help successfully loaded")
    
