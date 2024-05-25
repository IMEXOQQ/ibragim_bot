import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from database import get_lvl
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps

class ProfileSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    async def create_circular_image(self, img, size, border_size, border_color=(255, 255, 255)):
        # Увеличиваем размер для более качественного сглаживания
        large_size = size * 4
        large_border_size = border_size * 4

        img = img.resize((large_size, large_size), Image.LANCZOS)
        mask = Image.new('L', (large_size, large_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, large_size, large_size), fill=255)

        circular_img = ImageOps.fit(img, (large_size, large_size), method=Image.LANCZOS)
        circular_img.putalpha(mask)

        # Создаем изображение с обводкой
        border_size_with_image = large_size + 2 * large_border_size
        border = Image.new('RGBA', (border_size_with_image, border_size_with_image), (255, 255, 255, 0))
        mask = Image.new('L', (border_size_with_image, border_size_with_image), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, border_size_with_image, border_size_with_image), fill=255)
        border.paste(circular_img, (large_border_size, large_border_size), circular_img)

        # Рисуем обводку нужного цвета
        draw = ImageDraw.Draw(border)
        draw.ellipse((0, 0, border_size_with_image, border_size_with_image), outline=border_color, width=large_border_size // 5)
        
        # Уменьшаем изображение до конечного размера для лучшего сглаживания
        border = border.resize((size + 2 * border_size, size + 2 * border_size), Image.LANCZOS)
        
        return border



    @nextcord.slash_command(description="Вывод информации о пользователе")
    @commands.has_permissions(send_messages=True)
    async def profile(self, ctx, member: nextcord.Member = None):
        if member is None:
            member = ctx.user
        
        user_id = member.id
        guild_id = member.guild.id
        colour = member.color.to_rgb()

        row = await get_lvl(guild_id, user_id)
        experience = row[1]
        lvl = row[0]
        likes = row[2]
        progress = experience / (100*(lvl+1)*lvl)        
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content))

        # Создание круглой аватарки
        border_color = (255, 255, 255)
        avatar_with_border = await self.create_circular_image(avatar, 200, 10, border_color)

        # Создание изображения с градиентным фоном
        img = Image.new('RGB', (800, 400), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        for i in range(800):
            color = tuple(int(colour[j] * ((800 - i) / 800)) for j in range(3))
            draw.line((i, 0, i, 400), fill=color)
        
        # Добавление аватарки на фон
        img.paste(avatar_with_border, (40, 100), avatar_with_border)

        # Добавление текста
        font = ImageFont.truetype("boorsok.ttf", 48)
        draw.text((290, 100), f"{member.name}", font=font, fill=(255, 255, 255))
        draw.text((290, 180), f"Likes: {likes}", font=font, fill=(255, 255, 255))
        font = ImageFont.truetype("boorsok.ttf", 24)
        draw.text((640, 230), f"{int(progress*100)}%", font=font, fill=(255, 255, 255))

        # Добавление полосы загрузки
        progress_bar_width = 400
        progress_bar_height = 40
        progress_x = 290
        progress_y = 260
        draw.rectangle([progress_x, progress_y, progress_x + progress_bar_width, progress_y + progress_bar_height], outline=(255, 255, 255), width=4)
        draw.rectangle([progress_x, progress_y, progress_x + int(progress_bar_width * progress), progress_y + progress_bar_height], fill=(0, 255, 0))

        img = img.resize((400, 200), Image.LANCZOS)
        img.save('profile.png')
        
        await ctx.send(file=nextcord.File('profile.png'))

def setup(bot):
    bot.add_cog(ProfileSlash(bot))
    print("COGS | Module Profile_slash successfully loaded")