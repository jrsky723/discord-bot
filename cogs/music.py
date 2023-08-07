import discord
from discord import app_commands
from discord.ext import commands
import wavelink
from utils.utils import load_config


class Music(commands.GroupCog):
    vc: wavelink.Player = None

    async def join(self, interaction: discord.Interaction) -> bool:
        channel = interaction.user.voice.channel
        # if not channel:
        #     await interaction.response.send_message(f"Join a voice channel first.", delete_after=5)
        #     return False
        # if self.vc and self.vc.is_connected():
        #     await self.vc.disconnect()
        self.vc = await channel.connect(cls=wavelink.Player)
        self.vc.autoplay = True
        # await interaction.response.send_message(f"Joined {channel.name}.", delete_after=5)
        print('here!')
        # return True

    async def search(self, interaction: discord.Interaction, search: str) -> wavelink.YouTubeTrack:
        tracks = await wavelink.YouTubeTrack.search(search)
        if not tracks:
            await interaction.response.send_message(f"I could not find any songs with `{search}`")
            return None
        return tracks[0]

    @app_commands.command(description="Play the YouTube audio of the given search or URL.")
    async def play(self, interaction: discord.Interaction, *, search: str) -> None:
        # if not self.vc.is_connected():
        #     if not await self.join(interaction): return
            # await interaction.response.send_message(f"Join a voice channel first.", delete_after=5)
        if not self.vc: await self.join(interaction)
        track = await self.search(interaction, search=search)
        if not self.vc.is_playing():
            await self.vc.play(track, populate=True)
        else:
            await self.vc.queue.put_wait(track)
        await interaction.response.send_message(f"Playing {track.title}", delete_after=5)

    @app_commands.command(description="Skip.")
    async def skip(self, interaction: discord.Interaction) -> None:
        await self.vc.stop()
        await interaction.response.send_message(f"Skipped.", ephemeral=True, delete_after=5)

    @app_commands.command(description="Pause.")
    async def pause(self, interaction: discord.Interaction) -> None:
        await self.vc.pause()
        await interaction.response.send_message(f"Paused.", ephemeral=True, delete_after=5)

    @app_commands.command(description="Resume.")
    async def resume(self, interaction: discord.Interaction) -> None:
        await self.vc.resume()
        await interaction.response.send_message(f"Resumed.", ephemeral=True, delete_after=5)

    @app_commands.command(description="Stop and clear the queue.")
    async def stop(self, interaction: discord.Interaction) -> None:
        self.vc.queue.clear()
        await self.vc.stop()
        await interaction.response.send_message(f"Stopped.", ephemeral=True, delete_after=5)

    @app_commands.command(description="Set the volume to 0-100.")
    async def volume(self, interaction: discord.Interaction, volume: int) -> None:
        await self.vc.set_volume(volume)
        await interaction.response.send_message(f"Set volume to {volume}.", ephemeral=True, delete_after=5)

    @app_commands.command(description="Disconnect.")
    async def disconnect(self, interaction: discord.Interaction) -> None:
        await self.vc.disconnect()
        await interaction.response.send_message(f"Disconnected.", ephemeral=True, delete_after=5)

async def setup(bot: commands.Bot):
    config = load_config()
    node: wavelink.Node = wavelink.Node(uri="http://localhost:2333",
                                        password=config["PASSWORD"])
    await wavelink.NodePool.connect(client=bot, nodes=[node])
    await bot.add_cog(Music(name="m", description="Music commands."))
