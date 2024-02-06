import aiosqlite
from random import *

async def init_db():
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(
                "CREATE TABLE IF NOT EXISTS `guilds` ("
                "`id` INTEGER PRIMARY KEY AUTOINCREMENT,"
                "`guild_id` BIGINT NOT NULL"
                ")"
            )

            await cur.execute(
                "CREATE TABLE IF NOT EXISTS `roles` ("
                "`id` INTEGER PRIMARY KEY AUTOINCREMENT,"
                "`guild_id` BIGINT NOT NULL,"
                "`role_id` BIGINT NOT NULL,"
                "`update_time` INTEGER DEFAULT 72"
                ")"
            )

            await cur.execute(
                "CREATE TABLE IF NOT EXISTS `channels` ("
                "`id` INTEGER PRIMARY KEY AUTOINCREMENT,"
                "`guild_id` BIGINT NOT NULL,"
                "`channel_id` BIGINT NOT NULL"
                ")"
            )

            await cur.execute(
                "CREATE TABLE IF NOT EXISTS `users` ("
                "`id` INTEGER PRIMARY KEY AUTOINCREMENT,"
                "`guild_id` BIGINT NOT NULL,"
                "`user_id` BIGINT NOT NULL,"
                "`lvl` INTEGER DEFAULT 1,"
                "`xp` INTEGER DEFAULT 0,"
                "`total_likes` INTEGER DEFAULT 0"
                ")"
            )

            await db.commit()

async def add_guild(guild_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("INSERT INTO `guilds` (`guild_id`) VALUES (?)", (guild_id,))
            await db.commit()

async def get_all_guilds():
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("SELECT * FROM `guilds`")

            results = await cur.fetchall()
            return results

async def get_channel(guild_id: int, channel_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("SELECT guild_id, channel_id FROM `channels`")
            result = await cur.fetchall()
            if (guild_id, channel_id) in result:
                    return True
            else: return False

async def add_channel(guild_id: int, channel_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("INSERT INTO `channels`(`guild_id`, `channel_id`) VALUES (?, ?)", (guild_id, channel_id,))
            await db.commit()
            print(f"CHANNEL: {channel_id} added to main.db -> channels")

async def delete_channel(channel_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("DELETE FROM `channels` WHERE `channel_id`={}".format(channel_id,))
            await db.commit()
            print(f"CHANNEL: {channel_id} deleted from main.db -> channels")

async def get_user(guild_id: int, user_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("SELECT guild_id, user_id FROM `users`")
            result = await cur.fetchall()
            if (guild_id, user_id) not in result:
                    return False
            else: return True

async def get_users_ids(guild_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"SELECT user_id FROM `users` WHERE `guild_id`={guild_id}")
            result = await cur.fetchall()
            return result

async def add_user(guild_id: int, user_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("INSERT INTO `users`(`guild_id`, `user_id`) VALUES (?, ?)", (guild_id, user_id,))
            await db.commit()
            print(f"USER: {user_id} added to main.db -> users")

async def delete_user(guild_id: int, user_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"DELETE FROM `users` WHERE `guild_id`={guild_id} AND `user_id`={user_id}")
            await db.commit()
            print(f"USER: {user_id} deleted from main.db -> users")

async def get_role(guild_id: int, role_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("SELECT guild_id, role_id FROM `roles`")
            result = await cur.fetchall()
            if (guild_id, role_id) not in result:
                    return False
            else: return True

async def get_role_only_one(guild_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("SELECT guild_id FROM `roles`")
            result = await cur.fetchone()
            if result:
                    return True
            if not result: return False

async def get_guild_role(guild_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"SELECT role_id FROM `roles` WHERE `guild_id`={guild_id}")
            result = await cur.fetchone()
            role_id = result[0]
            return role_id

async def add_role(guild_id: int, role_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("INSERT INTO `roles`(`guild_id`, `role_id`) VALUES (?, ?)", (guild_id, role_id,))
            await db.commit()
            print(f"ROLE: {role_id} added to main.db -> roles")

async def delete_role(role_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute("DELETE FROM `roles` WHERE `role_id`={}".format(role_id,))
            await db.commit()
            print(f"ROLE: {role_id} deleted from main.db -> roles")

async def plus_like(guild_id: int, user_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"SELECT `total_likes` FROM `users` WHERE `guild_id`={guild_id} AND `user_id`={user_id}")
            row = await cur.fetchone()
            likes = row[0]
            await cur.execute(f"UPDATE `users` SET `total_likes`={likes+1} WHERE `guild_id`={guild_id} AND `user_id`={user_id}")
            await db.commit()
            print(f"Like: added like to {user_id} main.db -> users")

async def minus_like(guild_id: int, user_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"SELECT `total_likes` FROM `users` WHERE `guild_id`={guild_id} AND `user_id`={user_id}")
            row = await cur.fetchone()
            likes = row[0]
            if likes > 0:
                await cur.execute(f"UPDATE `users` SET `total_likes`={likes-1} WHERE `guild_id`={guild_id} AND `user_id`={user_id}")
            await db.commit()
            print(f"Like: removed like to {user_id} main.db -> users")

async def expierence(guild_id: int, user_id: int, content):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"SELECT `xp`,`lvl` FROM `users` WHERE `guild_id`={guild_id} AND `user_id`={user_id}")

            row = await cur.fetchone()
            xp = row[0]
            lvl = row[1]

            if 1<= len(content) <= 5:
                xp = xp + randint(1, 3)
            elif 6 <= len(content) <= 20:
                xp = xp + randint(5, 15)
            elif 21 <= len(content) <= 150:
                xp = xp + randint(25, 35)
            elif 151 <= len(content):
                xp+= 50

            await cur.execute(f"UPDATE `users` SET `xp`={xp} WHERE `guild_id`={guild_id} AND `user_id`={user_id}")

            lvl_after=int(xp/(lvl*100))
            flag = False
            if lvl < lvl_after:
                await cur.execute(f"UPDATE `users` SET `lvl`={lvl_after} WHERE `guild_id`={guild_id} AND `user_id`={user_id}")
                await cur.execute(f"UPDATE `users` SET `xp`={0} WHERE `guild_id`={guild_id} AND `user_id`={user_id}")
                print(f"USER: {user_id} updated to new lvl {lvl_after}")
                await cur.execute("SELECT * FROM `users` ORDER BY `lvl` DESC")
                flag = True
            await db.commit()
            return flag

async def get_lvl(guild_id: int, user_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"SELECT `lvl`, `xp`, `total_likes` FROM `users` WHERE `guild_id`={guild_id} AND `user_id`={user_id}")
            row = await cur.fetchone()
            return row

async def sorted_list_users(guild_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"SELECT * FROM `users` WHERE `guild_id`={guild_id} ORDER BY `lvl` DESC, 'xp' DESC")
            row = await cur.fetchall()
            return row

async def sorted_list_users_like(guild_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"SELECT * FROM `users` WHERE `guild_id`={guild_id} ORDER BY `total_likes` DESC")
            row = await cur.fetchall()
            return row

async def reset_lvl(guild_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"UPDATE `users` SET `lvl` = 1, `xp` = 0 WHERE `guild_id`={guild_id}")
            await db.commit()
            print(f"Guild:{guild_id} lvls was reseted main.db -> users")

async def reset_likes(guild_id: int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"UPDATE `users` SET `total_likes` = 0 WHERE `guild_id`={guild_id}")
            await db.commit()
            print(f"Guild:{guild_id} likes was reseted main.db -> users")

async def time_set(guild_id: int, hours):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"UPDATE `roles` SET `update_time` = {hours} WHERE `guild_id`={guild_id}")
            print(f"Roles: update time for guild:{guild_id} updated to {hours} hrs main.db -> roles")
            await db.commit()

async def get_time(guild_id: int, hours):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cur:
            await cur.execute(f"SELECT `update_time` FROM `roles` WHERE `guild_id` = {guild_id}")
            time = cur.fetchone
            return time[0]