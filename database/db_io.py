# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
# pylint: skip-file
"""Contains the functions to interact with the database"""

from .makedb import session_factory, Logs as dblog

class Logs:
    """Defines the log structure"""

    async def add_guild_log(
            self,
            guild_id: str,
            message_logging_channel_id: str,
            member_logging_channel_id: str,
            voice_logging_channel_id: str,
            moderation_logging_channel_id: str,
            muterole_role_id: str,
            muterole_logging_channel_id: str,) -> str:
        """Add a guild to the log table"""
        return "yes"

