import json


def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


async def get_messages(channel, limit: int):
    messages = [message async for message in channel.history(limit=limit)]
    return messages
