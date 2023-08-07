import discord
from discord.ext import commands
from discord import app_commands

class GeneralCog(commands.Cog):
    bot: commands.Bot = None

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(content="中国梦，实现伟大复兴", file=discord.File("resources/xi.jpg"))

    @app_commands.command()
    async def exit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("closing")
        await self.bot.close()

    @app_commands.command()
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("testing")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GeneralCog(bot))
