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