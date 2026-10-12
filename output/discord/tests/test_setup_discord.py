"""Offline checks using real discord.py models and a fake HTTP transport."""

import contextlib
import copy
import io
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import AsyncMock, patch

import discord

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import setup_discord as setup


class FakeHTTP:
    def __init__(self):
        self.next_id = 1000
        self.roles = [
            self.role_data(100, "@everyone", 0, discord.Permissions.none()),
            self.role_data(300, "Setup Bot", 10, setup.required_permissions()),
        ]
        self.channels = []
        self.writes = []
        self.create_role = AsyncMock(side_effect=self.add_role)
        self.create_channel = AsyncMock(side_effect=self.add_channel)
        self.edit_channel = AsyncMock(side_effect=self.move_channel)

    @staticmethod
    def role_data(role_id, name, position, permissions):
        return dict(id=str(role_id), name=name, position=position,
                    permissions=str(permissions.value), color=0,
                    hoist=False, managed=False, mentionable=False)

    async def add_role(self, guild_id, *, reason, **fields):
        self.next_id += 1
        data = self.role_data(self.next_id, fields["name"], 1,
                              discord.Permissions(int(fields["permissions"])))
        self.roles.append(data)
        self.writes.append(("role", copy.deepcopy(fields)))
        return data

    async def add_channel(self, guild_id, channel_type, *, reason, **fields):
        self.next_id += 1
        data = dict(id=str(self.next_id), type=channel_type, position=0,
                    bitrate=64000, user_limit=0, **fields)
        self.channels.append(data)
        self.writes.append(("channel", copy.deepcopy(data)))
        return data

    async def move_channel(self, channel_id, *, reason, **fields):
        channel = next(c for c in self.channels if int(c["id"]) == channel_id)
        channel.update(fields)
        self.writes.append(("edit_channel", copy.deepcopy(fields)))
        return channel


class ProvisionTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.http = FakeHTTP()
        self.client = discord.Client(intents=discord.Intents.none())
        self.state = self.client._connection
        self.state.http = self.http
        self.output = io.StringIO()

    def snapshot(self):
        guild = discord.Guild(state=self.state, data=dict(
            id="100", name="Phalom Test", owner_id="999", roles=self.http.roles,
            emojis=[], stickers=[], features=[],
        ))
        factories = {0: discord.TextChannel, 2: discord.VoiceChannel, 4: discord.CategoryChannel}
        channels = [factories[data["type"]](state=self.state, guild=guild, data=data)
                    for data in self.http.channels]
        member = discord.Member(state=self.state, guild=guild, data=dict(
            user=dict(id="200", username="Setup Bot", discriminator="0", avatar=None, bot=True),
            roles=["300"], joined_at="2026-10-12T00:00:00+00:00", flags=0,
        ))
        return guild, channels, member

    async def apply(self, *, apply=True, adopt_existing=False):
        with contextlib.redirect_stdout(self.output):
            return await setup.provision(*self.snapshot(), apply=apply, adopt_existing=adopt_existing)

    async def test_preview_has_no_writes(self):
        self.assertEqual(await self.apply(apply=False), (19, 0))
        self.assertEqual(self.http.writes, [])

    async def test_fresh_setup_and_rerun(self):
        self.assertEqual(await self.apply(), (19, 0))
        self.assertEqual(len(self.http.roles), 5)
        self.assertEqual(len(self.http.channels), 16)
        self.assertEqual(sum(c["type"] == 0 for c in self.http.channels), 10)
        self.assertEqual(sum(c["type"] == 2 for c in self.http.channels), 2)
        self.assertEqual(sum(c["type"] == 4 for c in self.http.channels), 4)
        writes = copy.deepcopy(self.http.writes)
        self.assertEqual(await self.apply(), (0, 19))
        self.assertEqual(self.http.writes, writes)

    async def test_partial_failure_can_resume(self):
        original = self.http.add_channel
        calls = 0

        async def fail_once(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 4:
                raise setup.SetupError("Simulated interrupted request")
            return await original(*args, **kwargs)

        self.http.create_channel.side_effect = fail_once
        with self.assertRaises(setup.SetupError):
            await self.apply()
        self.http.create_channel.side_effect = original
        self.assertEqual(await self.apply(), (13, 6))
        self.assertEqual(len(self.http.channels), 16)

    async def test_new_permissions_and_announcement_rules(self):
        await self.apply()
        guild, channels, bot_member = self.snapshot()
        roles = {r.name: r for r in guild.roles}
        everyone_id = str(guild.id)

        for channel in channels:
            overwrites = {entry.id: entry for entry in channel._overwrites}
            self.assertIn(int(everyone_id), overwrites)
            self.assertTrue(discord.Permissions(overwrites[guild.id].deny).view_channel)
            self.assertTrue(discord.Permissions(overwrites[roles["Guest / Mentor"].id].deny).view_channel)
            member = channel.overwrites_for(roles["Team Member"])
            lead = channel.overwrites_for(roles["Team Lead"])
            self.assertTrue(member.view_channel)
            self.assertTrue(lead.view_channel)
            if channel.name in {"announcements", "project-overview"}:
                self.assertFalse(member.send_messages)
                self.assertFalse(member.create_public_threads)
                self.assertTrue(member.send_messages_in_threads)
                self.assertTrue(lead.send_messages)
            else:
                self.assertTrue(member.send_messages)
        self.assertFalse(roles["Team Lead"].permissions.administrator)
        self.assertTrue(roles["Team Lead"].permissions.pin_messages)

    async def test_missing_permission_stops_before_writes(self):
        self.http.roles[1]["permissions"] = str(discord.Permissions(manage_channels=True).value)
        with self.assertRaisesRegex(setup.SetupError, "manage_roles"):
            await self.apply()
        self.assertEqual(self.http.writes, [])

    async def test_duplicate_role_stops_before_writes(self):
        for role_id in (401, 402):
            self.http.roles.append(self.http.role_data(role_id, "Team Member", 1, discord.Permissions.none()))
        with self.assertRaisesRegex(setup.SetupError, "Multiple role"):
            await self.apply()
        self.assertEqual(self.http.writes, [])

    async def test_misplaced_channel_stops_before_writes(self):
        self.http.channels.append(dict(id="700", name="general", type=0,
                                       position=0, parent_id=None, permission_overwrites=[]))
        with self.assertRaisesRegex(setup.SetupError, "outside"):
            await self.apply()
        self.assertEqual(self.http.writes, [])

    async def test_wrong_type_stops_before_writes(self):
        self.http.channels.append(dict(id="700", name="general", type=2,
                                       bitrate=64000, user_limit=0,
                                       position=0, parent_id=None, permission_overwrites=[]))
        with self.assertRaisesRegex(setup.SetupError, "different channel type"):
            await self.apply()
        self.assertEqual(self.http.writes, [])

    async def test_adopt_existing_general_preserves_id_and_topic(self):
        self.http.channels.append(dict(id="700", name="general", type=0,
                                       topic="Keep this existing topic", position=0,
                                       parent_id=None, permission_overwrites=[]))
        self.assertEqual(await self.apply(apply=False, adopt_existing=True), (18, 0))
        self.assertEqual(self.http.writes, [])
        self.assertEqual(await self.apply(adopt_existing=True), (18, 0))
        self.http.edit_channel.assert_awaited_once()
        general = next(c for c in self.http.channels if c["name"] == "general")
        category = next(c for c in self.http.channels if c["name"] == "TEAM SPACE")
        self.assertEqual(general["id"], "700")
        self.assertEqual(int(general["parent_id"]), int(category["id"]))
        self.assertEqual(general["topic"], "Keep this existing topic")
        self.assertTrue(general["permission_overwrites"])
        self.assertEqual(await self.apply(adopt_existing=True), (0, 19))

    async def test_existing_settings_preserved(self):
        await self.apply()
        self.http.roles[-1]["permissions"] = str(discord.Permissions(administrator=True).value)
        self.http.channels[1]["topic"] = "A human edited this."
        before = copy.deepcopy((self.http.roles, self.http.channels))
        await self.apply()
        self.assertEqual((self.http.roles, self.http.channels), before)

    async def test_wrong_application_stops_before_fetching_guild(self):
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.application_info.return_value = SimpleNamespace(id=1)
        with patch.object(setup.discord, "Client", return_value=mock_client):
            with self.assertRaisesRegex(setup.SetupError, "expected"):
                await setup.run(SimpleNamespace(guild_id=100, apply=True), "fake-test-value")
        mock_client.fetch_guild.assert_not_awaited()


class InputTests(unittest.TestCase):
    def test_preview_is_default(self):
        args = setup.parse_args(["--guild-id", "100"])
        self.assertFalse(args.apply)

    def test_application_id_is_not_server_id(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(setup.main(["--guild-id", str(setup.APPLICATION_ID)]), 2)


if __name__ == "__main__":
    unittest.main()
