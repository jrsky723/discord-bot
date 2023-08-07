import discord
from discord.ext import commands
from discord import app_commands
import random
from utils.utils import load_config


class ChatCog(commands.Cog):
    words: list[str] = []

    def __init__(self) -> None:
        config = load_config()
        self.words = config["WORDS"]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot: return
        if random.random() > 1 / 12: return
        word = random.choice(self.words)
        await message.channel.send(word)


async def setup(bot: commands.Bot):
    await bot.add_cog(ChatCog())
