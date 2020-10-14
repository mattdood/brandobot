import textwrap
import discord
from discord.ext import commands

class Helpers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def break_message(text: str, wrap_at=40, limit=2000):
        """
        Breaks long text from lines into 2,000 character chunks
        
        wrap_at and limit can be specified, without being overshot
        """
        messages = []
        for x in [text[i:i+limit] for i in range(0, len(text), limit)]:
           messages.append(x)
        return messages 

    @staticmethod
    def truncate_text(text: str, trunc_at=40):
        """
        Add elipses to the end of a long message as '...' to provide max lengths to messages.
        This is used to create the illusion of max-width on the `tabulate` library.
        A full-screen Discord client has a message window that is 60 characters wide.
        
        trunc_at can be specified, is defaulted to 40 characters
        """
        if len(text) > trunc_at:
            return text[:trunc_at]
        return text
