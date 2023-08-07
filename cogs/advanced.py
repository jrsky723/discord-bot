import discord
from discord.ext import commands
from discord import app_commands


class AdvancedCog(commands.Cog):
    bot: commands.Bot = None

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.cooldown(1, 60 * 15, key=lambda i: (i.guild.id))
    async def clone(self, interaction: discord.Interaction,
                    member: discord.Member) -> None:
        img = await member.display_avatar.read()
        await interaction.guild.me.edit(nick=member.display_name)
        await self.bot.user.edit(avatar=img)
        await interaction.response.send_message("낄낄")

    @app_commands.command()
    async def reset(self, interaction: discord.Interaction):
        await interaction.guild.me.edit(nick=None)
        await self.bot.user.edit(avatar=None)
        await interaction.response.send_message("Done", delete_after=5)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdvancedCog(bot))
