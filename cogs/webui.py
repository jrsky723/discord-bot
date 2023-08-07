import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import io
import base64

URL = "http://127.0.0.1:7860"


async def generate(prompt: str,
                   steps: int = 28,
                   width: int = 512,
                   height: int = 728) -> io.BytesIO:
    payload = {
        "prompt": prompt,
        "restore_faces": "true",
        "steps": steps,
        "width": width,
        "height": height,
        "cfg_scale": 8
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{URL}/sdapi/v1/txt2img",
                                json=payload) as response:
            r = await response.json()
            dat: str = r["images"][0]
            img = io.BytesIO(base64.b64decode(dat.split(",", 1)[0]))
    return img


class WebuiCog(commands.Cog):

    @app_commands.command(name="imgen")
    async def image(self,
                    interaction: discord.Interaction,
                    prompt: str,
                    steps: int = 28):
        await interaction.response.defer()
        f = await generate(prompt, steps)
        await interaction.followup.send(content=f"Prompt: {prompt}",
                                        file=discord.File(
                                        fp=f, filename="SPOILER_0.png"))


async def setup(bot: commands.Bot):
    await bot.add_cog(WebuiCog())
