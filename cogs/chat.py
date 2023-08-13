import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
from utils.utils import load_config


class ChatCog(commands.Cog):
    bot: commands.Bot = None
    words: list[str] = []
    channel: discord.TextChannel = None
    num_mentioned: int = 0

    def __init__(self, bot) -> None:
        config = load_config()
        self.bot = bot
        self.words = config["WORDS"]
        self.channel = self.bot.get_channel(config["TEXT_CHANNEL_ID"])
        self.background.start()

    def roll(self, num: int) -> bool:
        return random.random() < (1 / num)

    async def say(self, channel: discord.TextChannel, word: str) -> None:
        await channel.send(word)

    @commands.Cog.listener("on_message")
    async def respond(self, message: discord.Message) -> None:
        if message.author.bot: return
        if not self.roll(12): return
        word = random.choice(self.words)
        await self.say(message.channel, word)

    @commands.Cog.listener("on_message")
    async def on_mentioned(self, message: discord.Message) -> None:
        if message.author.bot: return
        count: int = 0
        for user in message.mentions:
            if self.bot.user == user: count += 1
        if count == 0: return
        self.num_mentioned += count
        if not self.roll(2): return
        await self.say(message.channel, '?' * (2 * self.num_mentioned - 1))
        self.num_mentioned = 0

    @tasks.loop(seconds=60)
    async def background(self):
        if not self.roll(60): return
        word = random.choice(self.words)
        await self.say(self.channel, word)


async def setup(bot: commands.Bot):
    await bot.add_cog(ChatCog(bot))
