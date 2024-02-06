import nextcord
import asyncio
from database import get_all_guilds, get_users_ids, get_guild_role, sorted_list_users, get_time
from nextcord.ext import commands, tasks
from settings import config


class UpdateRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.remove_roles.start()
        
    @tasks.loop(hours=72.0)
    async def remove_roles(self):
        #Убрать роль
        guild_data = await get_all_guilds()
        for guild_data_id in guild_data:
            guild = self.bot.get_guild(guild_data_id[1])
            if guild == None:
                continue
            else:
                try:
                    role_data_id = await get_guild_role(guild_data_id[1])
                except: continue
                if role_data_id != None:
                    role = nextcord.utils.get(guild.roles, id = role_data_id)
                    users_id_data = await get_users_ids(guild_data_id[1])
                    for user_data in users_id_data:
                        user_data_id = user_data[0]
                        member = guild.get_member(user_data_id)
                        if role in member.roles:
                            try:
                                await member.remove_roles(role)
                            except nextcord.HTTPException:
                                pass
            print(f"Role: roles for guild: {guild}:{guild_data_id[1]} REMOVED")
        #Добавить роль
        for guild_data_id in guild_data:
            guild = self.bot.get_guild(guild_data_id[1])
            if guild == None:
                continue
            else:
                try:
                    role_data_id = await get_guild_role(guild_data_id[1])
                except: continue
                if role_data_id != None:
                    role = nextcord.utils.get(guild.roles, id = role_data_id)
                    users_id_data = await sorted_list_users(guild_data_id[1])
                    for user_data in users_id_data[0:5]:
                        user_data_id = user_data[2]
                        member = guild.get_member(user_data_id)
                        if role not in member.roles:
                            try:
                                await member.add_roles(role)
                                print(member)
                            except nextcord.HTTPException:
                                pass
            print(f"Role: roles for guild: {guild}:{guild_data_id[1]}  ADDED")
            print(f"Role: roles for guild: {guild}:{guild_data_id[1]}  UPDATED")

    @remove_roles.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(UpdateRole(bot))
    print("COGS | Module Update_role successfully loaded")
