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



    async def create_round_image(self, img, size):
        img = img.convert("RGBA")

        img = img.resize((size, size), Image.LANCZOS)

        mask_size = (size*3, size*3)
        mask = Image.new('L', mask_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask_size[0], mask_size[1]), fill=255)
        
        mask = mask.resize((size, size), Image.LANCZOS)

        img.putalpha(mask)

        background = Image.new("RGBA", img.size, (255, 255, 255, 0))
        round_img = Image.alpha_composite(background, img)

        return round_img
    
    async def create_colored_circle_image(self, size, circle_color):
        img = Image.new("RGBA", (size*3, size*3), (255, 255, 255, 0))

        draw = ImageDraw.Draw(img)
        draw.ellipse((0,0,size*3,size*3), fill=circle_color)

        img = img.resize((size, size), Image.LANCZOS)

        return img
    
    async def create_progress_bar(self, width, height, progress):

        img = Image.new("RGBA", (width*3, height*3), (255, 255, 255, 0))

        draw = ImageDraw.Draw(img)
        border_radius = height // 2
        draw.rounded_rectangle([(0, 0), (width*3, height*3)], fill=(146, 160, 169, 255), outline="white", width=6*3, radius=22*3)
        if 0 <= progress <= 0.33:
            draw.rounded_rectangle([(18, 18), ((width-6)*3*progress, (height-6)*3)], fill=(7, 239, 44, 255), outline=None, width=6*3, radius=22*3)
        if 0.34 <= progress <= 0.74:
            draw.rounded_rectangle([(18, 18), ((width-6)*3*progress, (height-6)*3)], fill=(251, 205, 45, 255), outline=None, width=6*3, radius=22*3)
        if 0.75 <= progress <= 1:
            draw.rounded_rectangle([(18, 18), ((width-6)*3*progress, (height-6)*3)], fill=(251, 45, 45, 255), outline=None, width=6*3, radius=22*3)

        img = img.resize((width, height), Image.LANCZOS)

        return img

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
        progress = ((experience / (100*(lvl+1)*lvl)) // 0.01) / 100     
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content))

        # наложение круглой аватарки
        avatar = await self.create_round_image(avatar, 272)
        img = Image.open("./image/bg.png")
        img.paste(avatar, (64, 64), avatar)

        # наложение точки цвета роли
        dot = await self.create_colored_circle_image(28, colour)
        img.paste(dot, (380, 88), dot)

        # наложение полоску прогресса
        progress_bar = await self.create_progress_bar(1198, 42, progress)
        img.paste(progress_bar, (378, 296), progress_bar)

        # наложение текста
        font = ImageFont.truetype("./fonts/Inter-Bold.ttf", 64)
        drawer = ImageDraw.Draw(img)
        drawer.text((424, 64), f"{member.name.upper()}", font=font, fill="white")

        font = ImageFont.truetype("./fonts/Inter-Regular.ttf", 48)
        drawer.text((424, 144), f"Level: {lvl}", font=font, fill="white")
        drawer.text((720, 144), f"Likes: {likes}", font=font, fill="white")
        
        font = ImageFont.truetype("./fonts/Inter-Regular.ttf", 40)
        drawer.text((1500, 234), f"{int(progress*100)}%", font=font, fill="white")

        # изменение размера и сглаживание изображения    
        img = img.resize((823, 200), Image.LANCZOS)
        img.save('./image/profile.png')
        
        await ctx.send(file=nextcord.File('./image/profile.png'))

def setup(bot):
    bot.add_cog(ProfileSlash(bot))
    print("COGS | Module Profile_slash successfully loaded")