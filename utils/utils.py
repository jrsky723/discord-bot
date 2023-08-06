import json
import aiohttp
import io
import base64


def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


async def get_messages(channel, limit: int):
    messages = [message async for message in channel.history(limit=limit)]
    return messages


async def generate(prompt: str,
                   steps: int = 28,
                   width: int = 512,
                   height: int = 728) -> io.BytesIO:
    url = "http://127.0.0.1:7860"

    payload = {
        "prompt": prompt,
        "restore_faces": "true",
        "steps": steps,
        "width": width,
        "height": height,
        "cfg_scale": 8
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{url}/sdapi/v1/txt2img',
                                json=payload) as response:
            r = await response.json()
            dat: str = r['images'][0]
            img = io.BytesIO(base64.b64decode(dat.split(",", 1)[0]))
    return img
