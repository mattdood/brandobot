import os
import discord
import settings

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

client.run(settings.DISCORD_TOKEN)