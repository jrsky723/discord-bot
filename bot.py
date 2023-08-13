import discord
from discord.ext import commands
from utils.utils import load_config


class Bot(commands.Bot):

    def __init__(self) -> None:
        intents = discord.Intents.all()

        super().__init__(intents=intents, command_prefix='!')

    async def on_ready(self) -> None:
        print("Bot is ready.")
        await bot.load_extension(f"cogs.general")
        await bot.load_extension(f"cogs.advanced")
        await bot.load_extension(f"cogs.chat")
        # await bot.load_extension(f"cogs.webui")
        # await bot.load_extension(f"cogs.music")
        bot.tree.copy_global_to(guild=bot.guilds[0])
        await bot.tree.sync(guild=bot.guilds[0])


bot = Bot()

if __name__ == '__main__':
    config = load_config()
    bot.run(config["TOKEN"])
