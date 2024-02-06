import asyncio
import nextcord
import traceback
from settings import config
from settings.extensions import extensions
from nextcord.ext import commands
from database import init_db, get_all_guilds, add_guild



async def add_missing_guilds_to_db(bot: commands.Bot):
    guilds_data = await get_all_guilds()

    joined_guild_ids = [guild.id for guild in bot.guilds]
    guilds_ids = [guild_data[1] for guild_data in guilds_data]

    missing_guilds_ids = filter(lambda guild_id: guild_id not in guilds_ids, joined_guild_ids)

    for missing_guilds_id in missing_guilds_ids:
        await add_guild(missing_guilds_id)

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="%",
        help_command=None,
        intents=nextcord.Intents.all(),
        activity=nextcord.Game(name=f"Valorant")
    )

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

        await add_missing_guilds_to_db(self)

        print(f"Ready")

    async def on_guild_join(self, guild: nextcord.Guild):
        await add_guild(guild.id)
    



def main():
    loop = asyncio.get_event_loop()

    if loop.is_running():
        asyncio.ensure_future(run())
    else:
        loop.run_until_complete(run())

async def run():
    await init_db()

    discord_bot = DiscordBot()
    
    if __name__ == '__main__':
        for extension in extensions["extensions"]:
            try:
                discord_bot.load_extension(extension)
            except Exception as e:
                traceback.print_stack()
                print(f'ERROR | Could not load module "{e}"')
                
    await discord_bot.start(config.BOT_TOKEN)



main()
