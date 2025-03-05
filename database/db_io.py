# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""Contains the functions to interact with the database"""
from typing import Union
import sqlalchemy
from .makedb import session_factory, Logs as DbLog

class Logs:
    """Defines the log structure"""

    @staticmethod
    async def check_guild(guild_id: int) -> bool:
        """Checks if the guild is already in the database"""
        async with session_factory() as session:
            result = await session.query(DbLog).filter(DbLog.guild_id == guild_id).first()
            if result:
                return True
            return False

    @staticmethod
    async def add_guild_entry( # pylint: disable=R0913,R0917
            guild_id: str,
            message_logging_channel_id: str,
            member_logging_channel_id: str,
            voice_logging_channel_id: str,
            moderation_logging_channel_id: str,
            muterole_role_id: str,
            muterole_logging_channel_id: str,) -> str:
        """Add a guild to the log table"""
        async with session_factory() as session:
            guild_entry = await session.query(DbLog).filter(DbLog.guild_id == guild_id).first()
            if guild_entry:
                try:
                    setattr(guild_entry, "message_logging_channel_id", message_logging_channel_id)
                    setattr(guild_entry, "member_logging_channel_id", member_logging_channel_id)
                    setattr(guild_entry, "voice_logging_channel_id", voice_logging_channel_id)
                    setattr(guild_entry, "moderation_logging_channel_id", moderation_logging_channel_id)
                    setattr(guild_entry, "muterole_logging_channel_id", muterole_logging_channel_id)
                    setattr(guild_entry, "muterole_role_id", muterole_role_id)
                    await session.commit()
                    return "The operation completed successfully."
                except sqlalchemy.exc.SQLAlchemyError as e:
                    await session.rollback()
                    print(e)
                    return "Something went wrong, please check error logs."
            else:
                return "The guild does not exist."

    @staticmethod
    async def get_guild(guild_id: int) -> Union[DbLog, None, str]:
        """Gets a guild from the database"""
        async with session_factory() as session:
            try:
                entry: Union[DbLog, None] = await session.query(DbLog).filter(DbLog.guild_id == guild_id).first()
                if entry:
                    return entry
                return None

            except sqlalchemy.exc.SQLAlchemyError as e:
                print(e)
                return "Something went wrong, please check error logs."

    @staticmethod
    async def remove_guild(guild_id: int)-> str:
        """Removes a guild from the database"""
        async with session_factory() as session:
            try:
                entry = await session.query(DbLog).filter(DbLog.guild_id == guild_id).first()
                await session.delete(entry)
                await session.commit()
                return f"Guild with id {guild_id} was removed."

            except sqlalchemy.exc.SQLAlchemyError as e:
                print(e)
                return "Something went wrong, please check error logs."
