import discord
from dataclasses import dataclass
from typing import List

@dataclass
class Channel:
    """Ein Verteiler"""
    name: str
    # admins: List
    users: List
    tagets: List
    defaults: List

channels = [Channel("THM LoL", [455719785112666125], [903284136591102002, 903476955775656017], [("[LoL] Div 4", "THM Gaming")])]

client = discord.Client()

@client.event
async def on_message(message):
    print(message.author.id)
    if(message.author.id in channels[0].users):
        for target in channels[0].tagets:
            await client.get_channel(target).send("Test!")

client.run("OTAyOTY4OTU5ODkxMDIxODU0.YXmJYA.XjupU4G6BHohBtO9PlL6g41WNRA")