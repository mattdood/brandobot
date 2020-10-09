import os
import discord
import settings

if __name__ == '__main__':
    client = discord.Client()
    
    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord')
        guild = discord.utils.get(client.guilds, name=settings.DISCORD_GUILD)
        
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
    
    client.run(settings.DISCORD_TOKEN)
