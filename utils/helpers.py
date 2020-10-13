import textwrap

class Helpers:

    def text_wrap(text, wrap_at=40):
        """
        Wraps long text in equal 40 character (or less) lines
        
        wrap_at can be specified, without being overshot
        """
        paragraph = []
        for line in textwrap.wrap(text, wrap_at):
            paragraph.append(line)