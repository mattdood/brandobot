![Dio asset image](assets/img/dio-asset.jpeg)

# Overview
You thought this was a Discord bot, but **it was me, Dio!**

**BrandoBot** is a content curation Discord bot that allows users to interact with [Twitter](https://twitter.com) and [Reddit](https://reddit.com) directly through Discord. There are a few other misc. features coming soon. This is a *self-hosted bot*, check [**setup**](#Setup) for more details.

## Features
- `command_prefix` is `!`, this will be customizable in the future.
- **Twitter:**
  - Interact with Twitter timelines and lists, both as PMs and in text channels.
- **Reddit:**
  - Interact with Reddit subreddits, posts, and comments as PMs and in text channels.
- **General:**
  - Misc., helpful commands (*coming soon*)

## Setup
1. Install [Python](https://www.python.org/).
2. Create a virtual environment.
```
$ python3 -m venv .venv
```
3. Activate the virtual environment and install package requirements.
```
$ source .venv/bin/activate
$ pip install -r requirements/production.txt
```
4. Create your `.production` secrets file, then copy the contents of [`.envs/.local/.local`](.envs/.local/.local).
```
$ touch .envs/.production/.production
```
5. Make your bot account(s) and get your secrets prepared:
   * [Discord bot](https://discordpy.readthedocs.io/en/latest/discord.html)
   * [Twitter](https://developer.twitter.com/en/apply-for-access)
   * [Reddit](https://www.reddit.com/prefs/apps/)
     * [Follow the first half of this, down to 'create app'.](https://chatbotslife.com/how-to-build-a-reddit-bot-c890efb330c1)

## Future
* oblique strategies - brian eno & peter schmidt
* pollen count

# License
Released under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html) license.

No rights are claimed to [Dio Brando](https://en.wikipedia.org/wiki/Dio_Brando), the character from [Jojo's Bizarre Adventure](https://en.wikipedia.org/wiki/JoJo%27s_Bizarre_Adventure).

Artwork is not our own.

This project uses [discord.ext.menus](https://github.com/Rapptz/discord-ext-menus) package made by Danny Y. (Rapptz) which is distributed under MIT License.
Copy of this license can be found in [discord-ext-menus.LICENSE](brandobot/vendored/discord-ext-menus.LICENSE) file in [brandobot/vendored](brandobot/vendored) folder of this repository.
