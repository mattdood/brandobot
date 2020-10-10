"""
Settings for Brando Bot
"""
import os
from os.path import join
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve(strict=True).parent

ENV_PATH = join(ROOT_DIR, ".env/.production/.secrets")

# Loads the `.secrets` file
load_dotenv(ENV_PATH)

# Discord secrets
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD = os.getenv("DISCORD_GUILD")

# Twitter secrets
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")