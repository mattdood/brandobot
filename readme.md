# Brando Bot
![Dio asset image](assets/img/dio-asset.jpeg)

## Features
- `command_prefix` is `!`
  - use `!help` for a list of commands
- Subclass of `commands.Bot` -> `BrandoBot`
- Subclass of `commands.Cog` -> `GeneralCog`
  - Gives access to `GeneralCog` commands
- Subclass of `commands.Cog` -> `TwitterCog`
  - Gives access to `TwitterCog` commands

## Setup
1. Create venv `.env` and add `.production/.secrets`
```
python3 -m venv .env
touch .env/.production/.secrets
```
2. Add `DISCORD_TOKEN` and `DISCORD_GUILD` to secrets.
3. Start virtual env and run bot.
```
source .env/bin/activate
python bot.py
```

## Resources
[Discord.py](https://discordpy.readthedocs.io/)
[Discord.py Examples](https://github.com/Rapptz/discord.py)
[Official Python Discord bot](https://github.com/python-discord/bot)
[ModMail](https://github.com/kyb3r/modmail)
[Tweepy Twitter API](http://docs.tweepy.org/en/latest/api.html?highlight=list#list-methods)
[PRAW for Reddit](https://praw.readthedocs.io/en/latest/code_overview/models/comment.html)