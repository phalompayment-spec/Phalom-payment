#!/usr/bin/env python3
"""Create the Phalom Discord layout once, then disconnect.

Preview: python setup_discord.py --guild-id YOUR_SERVER_ID
Create:  python setup_discord.py --guild-id YOUR_SERVER_ID --apply
Token:   DISCORD_BOT_TOKEN environment variable, or a hidden interactive prompt.

Uses discord.py's HTTP methods; no Gateway connection, privileged intents,
slash commands, message posting, or permanently running bot is needed.
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass
import getpass
import os
import sys

import discord


APPLICATION_ID = 1558886738426990643
REASON = "Phalom / Sabaidee Merchant server setup"


@dataclass(frozen=True)
class ChannelSpec:
    name: str
    kind: str = "text"
    topic: str = ""
    leads_only: bool = False


LAYOUT = {
    "START HERE": (
        ChannelSpec("welcome", topic="Start here: introductions, working agreements, and where to post."),
        ChannelSpec("announcements", topic="Confirmed deadlines, meeting schedules, and important team updates. Reply in threads.", leads_only=True),
        ChannelSpec("project-overview", topic="Current brief, scope, milestones, and links to our latest materials. Suggest changes in threads.", leads_only=True),
    ),
    "TEAM SPACE": (
        ChannelSpec("general", topic="Daily conversation, quick questions, progress updates, and team support."),
        ChannelSpec("ideas", topic="Rough ideas welcome. One idea per message; discuss it in a thread."),
        ChannelSpec("research", topic="Merchant insights, competition, partners, and assumptions to test. Include sources and dates."),
    ),
    "PROJECT WORK": (
        ChannelSpec("tasks", topic="Agreed work with one owner, a due date, and a clear result. Update status in the task thread."),
        ChannelSpec("product-and-demo", topic="Merchant experience, payment flows, interface designs, and concept demos."),
        ChannelSpec("business-and-pitch", topic="Business model, costs, partners, slides, pitch script, and rehearsal feedback."),
        ChannelSpec("decisions-and-notes", topic="Agreed decisions and meeting notes, with owners, next actions, and discussion links."),
    ),
    "VOICE": (
        ChannelSpec("Team Room", kind="voice"),
        ChannelSpec("Focus Room", kind="voice"),
    ),
}

# Membership access is granted through category overwrites, so these roles
# do not grant ordinary members access to unrelated server channels.
ROLE_SPECS = {
    "Team Lead": (
        discord.Permissions(
            manage_channels=True, manage_messages=True, manage_threads=True,
            pin_messages=True, create_instant_invite=True,
        ),
        discord.Colour(0x147D7B),
    ),
    "Team Member": (discord.Permissions.none(), discord.Colour(0x5865F2)),
    "Guest / Mentor": (discord.Permissions.none(), discord.Colour(0xC79540)),
}

MEMBER_ACCESS = dict(
    view_channel=True, read_message_history=True, send_messages=True,
    add_reactions=True, embed_links=True, attach_files=True,
    create_public_threads=True, send_messages_in_threads=True,
    connect=True, speak=True, use_voice_activation=True,
)


class SetupError(Exception):
    """An actionable setup problem, safe to display without credentials."""


def positive_id(value: str) -> int:
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Enter a numeric Discord ID.") from exc
    if result <= 0:
        raise argparse.ArgumentTypeError("Discord IDs must be positive.")
    return result


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--guild-id", type=positive_id, required=True, help="Target SERVER ID, not the application ID.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Create missing resources. Otherwise only preview.")
    mode.add_argument("--dry-run", action="store_true", help="Explicitly preview without changes (the default).")
    parser.add_argument("--adopt-existing", action="store_true", help="Move matching channels from other categories into this layout and apply its channel permissions.")
    return parser.parse_args(argv)


def unique_named(items, name, label):
    matches = [item for item in items if item.name == name]
    if len(matches) > 1:
        raise SetupError(f"Multiple {label} items named {name!r}. Rename duplicates before rerunning.")
    return matches[0] if matches else None


def validate_existing(guild, channels, *, adopt_existing=False):
    """Reject ambiguous matches before creating anything."""
    categories = {}
    for name in ROLE_SPECS:
        role = unique_named(guild.roles, name, "role")
        if role and role.managed:
            raise SetupError(f"Role {name!r} is managed by an integration. Rename it or change ROLE_SPECS.")
    for category_name, specs in LAYOUT.items():
        category = unique_named(channels, category_name, "channel/category")
        if category is not None and not isinstance(category, discord.CategoryChannel):
            raise SetupError(f"{category_name!r} already exists but is not a category.")
        categories[category_name] = category
        for spec in specs:
            existing = unique_named(channels, spec.name, "channel")
            if existing is None:
                continue
            expected = discord.TextChannel if spec.kind == "text" else discord.VoiceChannel
            if not isinstance(existing, expected):
                raise SetupError(f"{spec.name!r} already exists with a different channel type.")
            if (category is None or existing.category_id != category.id) and not adopt_existing:
                raise SetupError(f"{spec.name!r} exists outside {category_name!r}. Rerun with --adopt-existing to move it and apply project channel permissions, or rename it manually.")
    return categories


def required_permissions():
    flags = {"manage_roles": True, "manage_channels": True, **MEMBER_ACCESS}
    for permissions, _colour in ROLE_SPECS.values():
        flags.update({name: True for name, enabled in permissions if enabled})
    return discord.Permissions(**flags)


def check_bot_permissions(bot_member):
    granted = bot_member.guild_permissions
    missing = [name for name, enabled in required_permissions() if enabled and not getattr(granted, name)]
    if missing:
        raise SetupError("The bot is missing server permissions: " + ", ".join(missing) + ". Grant them and rerun.")
    if bot_member.top_role.position <= 0:
        raise SetupError("Move the bot's role above @everyone so it can create roles below itself.")


def category_overwrites(guild, roles, bot_member):
    return {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        roles["Guest / Mentor"]: discord.PermissionOverwrite(view_channel=False),
        roles["Team Member"]: discord.PermissionOverwrite(**MEMBER_ACCESS),
        roles["Team Lead"]: discord.PermissionOverwrite(**MEMBER_ACCESS),
        # Explicit access lets setup work even when the new categories are private.
        bot_member: discord.PermissionOverwrite(view_channel=True, manage_channels=True),
    }


def channel_overwrites(guild, roles, bot_member, spec):
    overwrites = category_overwrites(guild, roles, bot_member)
    if spec.leads_only:
        overwrites[roles["Team Member"]] = discord.PermissionOverwrite(
            **{**MEMBER_ACCESS, "send_messages": False, "create_public_threads": False},
        )
        # Leads can start threads; members can reply in those threads.
    return overwrites


async def provision(guild, channels, bot_member, *, apply=False, adopt_existing=False):
    categories = validate_existing(guild, channels, adopt_existing=adopt_existing)
    check_bot_permissions(bot_member)
    roles = {}
    created = 0
    kept = 0
    moved = 0

    for name, (permissions, colour) in ROLE_SPECS.items():
        role = unique_named(guild.roles, name, "role")
        if role is not None:
            print(f"KEEP role: {name} (permissions unchanged)")
            if role.permissions != permissions:
                print("  NOTE: existing role permissions differ from this blueprint; review them manually.")
            kept += 1
        else:
            print(f"{'CREATE' if apply else 'WOULD CREATE'} role: {name}")
            created += 1
            if apply:
                role = await guild.create_role(
                    name=name, permissions=permissions, colour=colour,
                    hoist=name != "Guest / Mentor", mentionable=False, reason=REASON,
                )
        roles[name] = role

    for category_name, specs in LAYOUT.items():
        category = categories[category_name]
        if category is not None:
            print(f"KEEP category: {category_name} (settings unchanged)")
            kept += 1
        else:
            print(f"{'CREATE' if apply else 'WOULD CREATE'} category: {category_name}")
            created += 1
            if apply:
                category = await guild.create_category(
                    category_name, overwrites=category_overwrites(guild, roles, bot_member), reason=REASON,
                )

        for spec in specs:
            existing = unique_named(channels, spec.name, "channel")
            if existing is not None:
                original_category = categories[category_name]
                needs_move = original_category is None or existing.category_id != original_category.id
                if needs_move:
                    print(f"  {'MOVE' if apply else 'WOULD MOVE'} {spec.kind}: {spec.name} -> {category_name} (apply project channel permissions)")
                    if apply:
                        await existing.edit(
                            category=category,
                            overwrites=channel_overwrites(guild, roles, bot_member, spec),
                            reason=REASON,
                        )
                    moved += 1
                    continue
                print(f"  KEEP {spec.kind}: {spec.name} (settings unchanged)")
                kept += 1
                continue
            print(f"  {'CREATE' if apply else 'WOULD CREATE'} {spec.kind}: {spec.name}")
            created += 1
            if apply:
                kwargs = dict(
                    category=category,
                    overwrites=channel_overwrites(guild, roles, bot_member, spec),
                    reason=REASON,
                )
                if spec.kind == "text":
                    await guild.create_text_channel(spec.name, topic=spec.topic, **kwargs)
                else:
                    await guild.create_voice_channel(spec.name, **kwargs)

    print(f"\n{'Created' if apply else 'Would create'} {created} items; kept {kept} existing items; {'moved' if apply else 'would move'} {moved} channels.")
    if apply:
        print("Assign Team Member to teammates and Team Lead to leads in Discord.")
        print("Guest / Mentor has no project access until you explicitly grant a channel.")
        print("The server owner always retains access; a separate Server Owner role is unnecessary.")
        print("Setup finished. You can remove the bot; the created roles and channels remain.")
    else:
        print("Preview only. Rerun with --apply to create the missing items.")
    return created, kept


async def run(args, token):
    # login() authenticates HTTP requests; start()/run() would also open a
    # Gateway connection, which this one-time job does not need.
    async with discord.Client(intents=discord.Intents.none()) as client:
        await client.login(token)
        app = await client.application_info()
        if app.id != APPLICATION_ID:
            raise SetupError(f"This token belongs to application {app.id}, expected {APPLICATION_ID}.")
        guild = await client.fetch_guild(args.guild_id)
        if client.user is None:
            raise SetupError("The authenticated bot identity is unavailable.")
        bot_member = await guild.fetch_member(client.user.id)
        channels = await guild.fetch_channels()
        print(f"Bot: {client.user} | Application: {app.id}")
        print(f"Target server: {guild.name} ({guild.id})")
        print(f"Mode: {'APPLY' if args.apply else 'PREVIEW'}\n")
        await provision(guild, channels, bot_member, apply=args.apply, adopt_existing=args.adopt_existing)


def main(argv=None):
    args = parse_args(argv)
    if args.guild_id == APPLICATION_ID:
        print("ERROR: --guild-id must be the target server ID, not the application ID.", file=sys.stderr)
        return 2
    token = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
    if not token:
        if not sys.stdin.isatty():
            print("ERROR: Set DISCORD_BOT_TOKEN or run in an interactive terminal for a hidden prompt.", file=sys.stderr)
            return 2
        token = getpass.getpass("Discord bot token (hidden): ").strip()
    if not token:
        print("ERROR: A bot token is required; the application ID and public key cannot authenticate.", file=sys.stderr)
        return 2
    try:
        asyncio.run(run(args, token))
    except discord.LoginFailure:
        print("ERROR: Invalid bot token. Get the bot token from your application's Bot settings.", file=sys.stderr)
        return 1
    except discord.Forbidden:
        print("ERROR: Discord denied access. Check the server ID, bot membership, permissions, and role hierarchy.", file=sys.stderr)
        print("Earlier creations may remain. Correct access and rerun; existing items are preserved.", file=sys.stderr)
        return 1
    except discord.NotFound:
        print("ERROR: Server or resource not found. Check the server ID and bot membership.", file=sys.stderr)
        return 1
    except discord.HTTPException as exc:
        # Do not print request details or credentials.
        print(f"ERROR: Discord API failure (HTTP {exc.status}, code {exc.code}). Correct the problem and rerun.", file=sys.stderr)
        return 1
    except SetupError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except (OSError, asyncio.TimeoutError):
        print("ERROR: Network connection failed. Check connectivity and rerun.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nStopped. Existing items are preserved; rerun to finish.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
