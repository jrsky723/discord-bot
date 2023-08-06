import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import generate
import random

class AdvancedCog(commands.Cog):
    bot: commands.Bot = None

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.cooldown(1, 60 * 15, key=lambda i: (i.guild.id))
    async def clone(self, interaction: discord.Interaction, member: discord.Member) -> None:
        img = await member.display_avatar.read()
        await interaction.guild.me.edit(nick=member.display_name)
        await self.bot.user.edit(avatar=img)
        await interaction.response.send_message("낄낄")

    @app_commands.command()
    async def reset(self, interaction: discord.Interaction):
        await interaction.guild.me.edit(nick=None)
        await self.bot.user.edit(avatar=None)
        await interaction.response.send_message("Done", delete_after=5)

    @app_commands.command(name="img")
    async def image(self,
                    interaction: discord.Interaction,
                    prompt: str,
                    steps: int = 28):
        await interaction.response.defer()
        f = await generate(prompt, steps)
        await interaction.followup.send(content=f"Prompt: {prompt}", file=discord.File(fp=f, filename="SPOILER_0.png"))

async def on_message(message: discord.Message) -> None:
    if message.author.bot: return
    if random.random() > 1/12: return
    word = random.choice(on_message.words)
    await message.channel.send(word)
on_message.words = [
    "어휴", "사람살려", "진좆", "진큰", "아이고", "총질 ㄱ", "?", "??", "???", "시작", "출발",
    "ㄹㅇ", "ㄹㅇㅋㅋ", "뒤지고싶나", "씹", "찍", "좆됐네 진짜", "떼잉", "허허", "훠훠", "뭐라도 ㄱ",
    "두삼딩", "아 안되겠다", "슬슬 준비해야 쓰겄다", "맞지", "옳지"
] + ["ㅋ" * l for l in range(2, 5)]

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdvancedCog(bot))
    bot.add_listener(on_message)
