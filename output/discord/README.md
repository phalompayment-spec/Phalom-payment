# Phalom Discord setup

One-time setup for **Phalom | Sabaidee Merchant**, using the bot already invited to your server.

Creates **3 roles**, **4 categories**, **10 text channels**, and **2 voice channels** matching the team blueprint.

## Run on Windows / PowerShell

Use Python 3.10 or newer.

```powershell
Set-Location 'C:\Users\phetm\Projects\phalom\output\discord'
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Replace the number below with YOUR SERVER ID.
# The script prompts for your bot token without displaying it.
.\.venv\Scripts\python.exe setup_discord.py --guild-id 123456789012345678 --dry-run --adopt-existing

# Create the missing items after reviewing the preview.
.\.venv\Scripts\python.exe setup_discord.py --guild-id 123456789012345678 --apply --adopt-existing
```

The server ID is different from application ID **1558886738426990643**. Enable Developer Mode in Discord's Advanced settings, then right-click your server and choose **Copy Server ID**.

The commands above include `--adopt-existing` so a pre-existing `#general` can be moved into TEAM SPACE. Any matching channel outside its intended category will be moved, retaining its messages and topic, and will receive the project channel permissions. Omit this flag if you want such a collision to stop setup instead. Unrelated channels and empty default categories are left in place.

Get the token from your application in the [Discord Developer Portal](https://discord.com/developers/applications/1558886738426990643/bot). The supplied public key is for verifying incoming interaction requests and is not used here. Paste the **bot token** into the script's hidden prompt, not into the source or chat.

For unattended execution, set `DISCORD_BOT_TOKEN` in the process environment using your preferred secret-management mechanism. The script reads that variable before prompting. There is intentionally no command-line token argument or token file.

## Bot permissions

Before applying, ensure the bot has the following server permissions. The script checks them before creating anything and prints missing permission names.

- Manage Channels and Manage Roles.
- Manage Messages, Manage Threads, Pin Messages, and Create Invite, so it can grant those capabilities to Team Lead.
- View Channels, Read Message History, Send Messages, Add Reactions, Embed Links, Attach Files, Create Public Threads, and Send Messages in Threads.
- Connect, Speak, and Use Voice Activity.

Place the bot's role above the roles it needs to create/manage. New roles are created below the bot. An existing Administrator permission also satisfies the permission check; the script does not grant Administrator to anyone.

## Access after setup

- New categories and channels are private to Team Lead, Team Member, the server owner, administrators, and the setup bot.
- Assign **Team Member** to your teammates manually in Server Settings → Members.
- Assign **Team Lead** to your coordinators. Either team role gives project access.
- **Guest / Mentor** has no project access until you explicitly grant individual channels. A person who also has Team Member or Team Lead retains that team access.
- Team Lead can post in `announcements` and `project-overview`; Team Member can read and reply in threads created by leads.
- No separate Server Owner role is created: Discord ownership already provides access.
- Team Lead's management permissions apply at server level. Use this layout in your dedicated project server.

## What reruns do

- No changes happen unless you pass `--apply`.
- Existing roles and channels with the same exact names and expected locations are kept. Their permissions, topics, and settings are not overwritten.
- Existing role permission differences produce a review note. Existing categories/channels retain their current privacy; review their permissions if you are adopting an older server.
- Duplicate names, integration-managed role collisions, and wrong channel types stop setup before the first creation. Channels in unexpected categories also stop setup unless `--adopt-existing` is supplied.
- No channels, roles, or messages are deleted. The server is not renamed. No roles are assigned to people automatically.
- It does not post welcome messages or upload project files. Copy those from the companion server blueprint when ready.
- Discord applies each creation separately. If a later request fails, completed creations remain; fix the reported issue and rerun. Run only one setup process at a time.

After checking the layout and assigning team roles, remove the bot from the server. The created structure remains. This script exits on its own after setup and needs no hosting or privileged Gateway intents.

## Checks

Offline checks use fake Discord objects and make no API requests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## References

- [discord.py installation](https://discordpy.readthedocs.io/en/stable/intro.html#installing)
- [discord.py API](https://discordpy.readthedocs.io/en/stable/api.html)
- [Discord permission rules and role hierarchy](https://docs.discord.com/developers/topics/permissions)
- [Discord application credentials](https://github.com/discord/discord-api-docs/blob/main/developers/quick-start/getting-started.mdx)

## Version log

- 2026-10-12: Initial Phalom setup script and PowerShell instructions.
