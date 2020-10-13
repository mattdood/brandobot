import textwrap
import discord
from discord.ext import commands

class Helpers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def wrap_message(text: str, wrap_at=40):
        """
        Wraps long text in equal 40 character (or less) lines
        
        wrap_at can be specified, without being overshot
        """
        paragraph = []
        for line in textwrap.wrap(text, wrap_at):
            paragraph.append(line)
        return paragraph

    @staticmethod
    def break_message(text: str, wrap_at=40, limit=2000):
        """
        Breaks long text from lines into 2,000 character chunks
        
        wrap_at and limit can be specified, without being overshot
        """
        text = Helpers.wrap_message(text=text, wrap_at=40)
        message = []
        messages = []
        i = 0
        for line in text:
            while i < limit/int(len(line) * wrap_at):
                message.append(line)
                i += 1
            else:
                messages.append(message)
        return messages