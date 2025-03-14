# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""Contains the functions to interact with the database"""
from typing import Union, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.logger import logger
from .makedb import session_factory, Logs as DbLog, Punishments as DbPunishments, CustomCommands as DbCc

class Logs:
    """Defines the log structure"""

    @staticmethod
    async def _get_guild_entry(guild_id: int, session: Session) -> Union[DbLog, None]:
        """Helper method to get a guild entry"""
        return (await session.execute(select(DbLog).where(DbLog.guild_id == guild_id))).scalars().first()


    @staticmethod
    async def check_guild(guild_id: int) -> bool:
        """Checks if the guild is already in the database"""
        async with session_factory() as session:
            return await Logs._get_guild_entry(guild_id, session) is not None


    @staticmethod
    async def get_guild(guild_id: int) -> Union[DbLog, None, str]:
        """Gets a guild from the database"""
        async with session_factory() as session:
            try:
                return await Logs._get_guild_entry(guild_id, session)
            except SQLAlchemyError as e:
                logger.error("Database error while getting guild entry: %s", e, exc_info=True)
                return "Something went wrong, please check error logs."


    @staticmethod
    async def remove_guild(guild_id: int)-> str:
        """Removes a guild from the database"""
        async with session_factory() as session:
            try:
                entry = await Logs._get_guild_entry(guild_id, session)
                if entry is None:
                    return f"Guild with id {guild_id} does not exist."
                await session.delete(entry)
                await session.commit()
                return f"Guild with id {guild_id} was removed."

            except SQLAlchemyError as e:
                if session.in_transaction():
                    await session.rollback()
                logger.error("Database error while removing guild entry: %s\nRolling back...", e, exc_info=True)
                return "Something went wrong, please check error logs."


    @staticmethod
    async def add_guild_on_join(guild_id: int) -> str:
        """Adds a guild to the log table"""
        async with session_factory() as session:
            try:
                guild_entry = DbLog(guild_id=guild_id)
                await session.add(guild_entry)
                await session.commit()
                return f"Guild with id {guild_id} added to the database successfully."

            except SQLAlchemyError as e:
                if session.in_transaction():
                    await session.rollback()
                logger.error("Database error while adding guild entry on guild join: %s\nRolling back...", e, exc_info=True)
                return "Something went wrong, please check error logs."


    @staticmethod
    async def update_guild(guild_id: int, **kwargs: Any) -> str:
        """Updates a guild's log entry"""
        async with session_factory() as session:
            guild_entry = await Logs._get_guild_entry(guild_id, session)
            if guild_entry:
                try:
                    valid_fields = {c.name for c in DbLog.__table__.columns}
                    updates = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}
                    for key, value in updates.items():
                        setattr(guild_entry, key, value)

                    await session.commit()
                    return "The operation completed successfully."
                except SQLAlchemyError as e:
                    if session.in_transaction():
                        await session.rollback()
                    logger.error("Database error while updating guild entry: %s\nRolling back...", e, exc_info=True)
                    return "Something went wrong, please check error logs."
            else:
                return "The guild does not exist."


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

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error("Database error while adding punishment entry: %s", e, exc_info=True)
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
            except SQLAlchemyError as e:
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

            except SQLAlchemyError as e:
                await session.rollback()
                print(e)
                return "Something went wrong, please check error logs."


class CustomCommands: # pylint: disable=R0903
    """Defines the custom commands structure"""


    @staticmethod
    async def add_custom_command(name: str, owner_id: str, text: str, image: bytes, nsfw: bool) -> str:
        """Adds a custom command to the database"""
        try:
            async with session_factory() as session:
                custom_command_entry = DbCc()
                setattr(custom_command_entry, "name", name)
                setattr(custom_command_entry, "owner_id", owner_id)
                setattr(custom_command_entry, "text", text)
                setattr(custom_command_entry, "image", image)
                setattr(custom_command_entry, "nsfw", nsfw)
                await session.add(custom_command_entry)
                await session.commit()
                return "The custom command was added to the database successfully."

        except SQLAlchemyError as e:
            if session.in_transaction():
                await session.rollback()
            logger.error("Database error while adding custom command: %s\nRolling back....", e, exc_info=e)
            return "Something went wrong, please check error logs."
