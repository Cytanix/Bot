# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""Contains the functions to interact with the database"""
from typing import Union
import sqlalchemy
from sqlalchemy import select
from .makedb import session_factory, Logs as DbLog, Punishments as DbPunishments

class Logs:
    """Defines the log structure"""

    @staticmethod
    async def check_guild(guild_id: int) -> bool:
        """Checks if the guild is already in the database"""
        async with session_factory() as session:
            result = (await session.execute(select(DbLog).filter(DbLog.guild_id == guild_id))).scalars().first()
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
            guild_entry = (await session.execute(select(DbLog).filter(DbLog.guild_id == guild_id))).scalars().first()
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
                entry: Union[DbLog, None] = (await session.execute(select(DbLog).filter(DbLog.guild_id == guild_id))).scalars().first()
                if entry:
                    return entry
                return None

            except sqlalchemy.exc.SQLAlchemyError as e:
                await session.rollback()
                print(e)
                return "Something went wrong, please check error logs."

    @staticmethod
    async def remove_guild(guild_id: int)-> str:
        """Removes a guild from the database"""
        async with session_factory() as session:
            try:
                entry = (await session.execute(select(DbLog).filter(DbLog.guild_id == guild_id))).scalars().first()
                await session.delete(entry)
                await session.commit()
                return f"Guild with id {guild_id} was removed."

            except sqlalchemy.exc.SQLAlchemyError as e:
                await session.rollback()
                print(e)
                return "Something went wrong, please check error logs."

    @staticmethod
    async def add_guild_on_join(guild_id: int) -> str:
        """Adds a guild to the log table"""
        try:
            async with session_factory() as session:
                guild_entry = DbLog()
                setattr(guild_entry, "guild_id", guild_id)
                await session.add(guild_entry)
                await session.commit()
                return f"Guild with id {guild_id} added to the database successfully."

        except sqlalchemy.exc.SQLAlchemyError as e:
            await session.rollback()
            print(e)
            return "Something went wrong, please check error logs."

class Punishments:
    """Defines the punishment structure"""

    @staticmethod
    async def add_punishment( # pylint: disable=R0913,R0917
            guild_id: int,
            user_id: int,
            punishment: str,
            punishment_time: int,
            moderator_id: int,
            reason: str,) -> str:
        """Adds a punishment to the database"""
        try:
            async with session_factory() as session:
                punishment_entry = DbPunishments()
                setattr(punishment_entry, "guild_id", guild_id)
                setattr(punishment_entry, "user_id", user_id)
                setattr(punishment_entry, "punishment", punishment)
                setattr(punishment_entry, "punishment_time", punishment_time)
                setattr(punishment_entry, "moderator_id", moderator_id)
                setattr(punishment_entry, "reason", reason)
                await session.add(punishment_entry)
                await session.commit()
                return "The punishment was added to the database successfully."

        except sqlalchemy.exc.SQLAlchemyError as e:
            await session.rollback()
            print(e)
            return "Something went wrong, please check error logs."

    @staticmethod
    async def get_punishment(punishment_id: int, guild_id: int, user_id: int) -> Union[DbPunishments, None, str]:
        """Gets a punishment from the database"""
        async with session_factory() as session:
            try:
                entry: Union[DbPunishments, None] = (await session.execute(select(DbPunishments).filter(
                    DbPunishments.punishment_id == punishment_id,
                    DbPunishments.guild_id == guild_id,
                    DbPunishments.user_id == user_id))).scalars().first()
                if entry:
                    return entry
                return None
            except sqlalchemy.exc.SQLAlchemyError as e:
                await session.rollback()
                print(e)
                return "Something went wrong, please check error logs."

    @staticmethod
    async def delete_punishment(punishment_id: int) -> str:
        """Deletes a punishment from the database"""
        async with session_factory() as session:
            try:
                entry = (await session.execute(select(DbPunishments).filter(DbPunishments.punishment_id == punishment_id))).scalars().first()
                if entry:
                    await session.delete(entry)
                    await session.commit()
                    return "The punishment was deleted successfully."

                return "There was an error deleting the punishment."

            except sqlalchemy.exc.SQLAlchemyError as e:
                await session.rollback()
                print(e)
                return "Something went wrong, please check error logs."
