# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""Contains the functions to interact with the database"""
import traceback
from typing import Union, Any, cast
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from utils.logger import logger
from utils.error_reporting import send_error
from database.makedb import session_factory, Logs as DbLog, Punishments as DbPunishments, CustomCommands as DbCc


class Logs:
    """Defines the log structure"""

    @staticmethod
    async def _get_guild_entry(guild_id: int, session: AsyncSession) -> Union[DbLog, None]:
        """Helper method to get a guild entry"""
        result = await session.execute(select(DbLog).filter(DbLog.guild_id == guild_id))
        if result:
            return cast(DbLog, result.scalars().first())
        return None

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
                tb_str = traceback.format_exc()
                await send_error("get_guild", f"{str(e)}\n{tb_str}")
                logger.error("Database error while getting guild entry: %s", e, exc_info=True)
                return "Something went wrong, please check error logs."

    @staticmethod
    async def remove_guild(guild_id: int) -> str:
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
                tb_str = traceback.format_exc()
                await send_error("remove_guild", f"{str(e)}\n{tb_str}")
                if session.is_active:
                    await session.rollback()
                logger.error("Database error while removing guild entry: %s\nRolling back...", e, exc_info=True)
                return "Something went wrong, please check error logs."

    @staticmethod
    async def add_guild_on_join(guild_id: int) -> str:
        """Adds a guild to the log table"""
        async with session_factory() as session:
            try:
                guild_entry = DbLog(guild_id=guild_id)
                if guild_entry is None:
                    return "No guild entry"
                if session is None:
                    return "No session"
                session.add(guild_entry)
                await session.commit()
                return f"Guild with id {guild_id} added to the database successfully."

            except SQLAlchemyError as e:
                tb_str = traceback.format_exc()
                await send_error("add_guild_on_join", f"{str(e)}\n{tb_str}")
                if session.is_active:
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
                    tb_str = traceback.format_exc()
                    await send_error("update_guild", f"{str(e)}\n{tb_str}")
                    if session.is_active:
                        await session.rollback()
                    logger.error("Database error while updating guild entry: %s\nRolling back...", e, exc_info=True)
                    return "Something went wrong, please check error logs."
            else:
                return "The guild does not exist."


class Punishments:
    """Defines the punishment structure"""

    @staticmethod
    async def _get_punishment_entry(punishment_id: int, session: AsyncSession) -> Union[DbPunishments, None]:
        """Helper method to get a punishment entry"""
        result = await session.execute(select(DbPunishments).filter(DbPunishments.punishment_id == punishment_id))
        return cast(Union[DbPunishments, None], result.scalars().first())


    @staticmethod
    async def add_punishment(**kwargs: Any) -> str:
        """Adds a punishment to the database"""
        async with session_factory() as session:
            try:
                punishment_entry = DbPunishments()
                valid_fields = {c.name for c in DbPunishments.__table__.columns}
                updates = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}
                for key, value in updates.items():
                    setattr(punishment_entry, key, value)
                session.add(punishment_entry)
                await session.commit()
                return "The punishment was added to the database successfully."

            except SQLAlchemyError as e:
                tb_str = traceback.format_exc()
                await send_error("add_punishment", f"{str(e)}\n{tb_str}")
                if session.is_active:
                    await session.rollback()
                logger.error("Database error while adding punishment entry: %s", e, exc_info=True)
                return "Something went wrong, please check error logs."


    @staticmethod
    async def get_punishment(punishment_id: int, guild_id: int) -> Union[DbPunishments, str]:
        """Gets a punishment from the database"""
        async with session_factory() as session:
            try:
                entry = await Punishments._get_punishment_entry(punishment_id, session)
                if entry:
                    if entry.guild_id == guild_id:
                        return entry
                    return ("Unable to find entry. Are you sure you have the correct ID.\n"
                            "-# Please note, punishments can only be viewed in the guild they came from.")
                return "Punishment not found."
            except SQLAlchemyError as e:
                tb_str = traceback.format_exc()
                await send_error("get_punishment", f"{str(e)}\n{tb_str}")
                logger.error("Database error while getting punishment entry: %s", e, exc_info=True)
                return "Something went wrong, please check error logs."


    @staticmethod
    async def delete_punishment(punishment_id: int, guild_id: int) -> str:
        """Deletes a punishment from the database"""
        async with session_factory() as session:
            try:
                entry = await Punishments._get_punishment_entry(punishment_id, session)
                if entry is None:
                    return "Punishment not found."
                if entry.guild_id == guild_id:
                    await session.delete(entry)
                    await session.commit()
                    return "The punishment was deleted successfully."

                return "There was an error deleting the punishment."

            except SQLAlchemyError as e:
                tb_str = traceback.format_exc()
                await send_error("delete_punishment", f"{str(e)}\n{tb_str}")
                if session.is_active:
                    await session.rollback()
                logger.error("Database error while deleting punishment: %s\nRolling back...", e, exc_info=True)
                return "Something went wrong, please check error logs."

    @staticmethod
    async def get_punishments_by_user(user_id: int, guild_id: int) -> Union[DbPunishments, str]:
        """Gets punishments by user"""
        async with session_factory() as session:
            result = await session.execute(
                select(DbPunishments).filter(
                    DbPunishments.user_id == user_id,
                    DbPunishments.guild_id == guild_id
                )
            )
            if result:
                return cast(DbPunishments, result.scalars().all())
            return "There was an error getting punishments by user or that user has no punishments."


class CustomCommands: # pylint: disable=R0903
    """Defines the custom commands structure"""

    @staticmethod
    async def _get_command_entry(name: str, session: AsyncSession) -> Union[DbCc, None]:
        """Helper method to get a command entry"""
        result = await session.execute(DbCc).filter(DbCc.name == name)
        return cast(Union[DbCc, None], result.scalars().first())

    @staticmethod
    async def add_custom_command(**kwargs: Any  ) -> str:
        """Adds a custom command to the database"""
        async with session_factory() as session:
            try:
                valid_fields = {c.name for c in DbCc.__table__.columns}
                updates = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}

                custom_command_entry = DbCc(**updates)
                session.add(custom_command_entry)
                await session.commit()

                return "The custom command was added to the database successfully."

            except SQLAlchemyError as e:
                tb_str = traceback.format_exc()
                await send_error("add_custom_command", f"{str(e)}\n{tb_str}")
                if session.is_active:
                    await session.rollback()
                logger.error("Database error while adding custom command: %s\nRolling back....", e, exc_info=True)
                return "Something went wrong, please check error logs."

    @staticmethod
    async def get_custom_command(name: str) -> Union[DbCc, None]:
        """Gets a custom command from the database"""
        async with session_factory() as session:
            entry = await CustomCommands._get_command_entry(name, session)
            return entry or None

    @staticmethod
    async def edit_custom_command(name: str, **kwargs: Any) -> str:
        """Edits a custom command from the database"""
        async with session_factory() as session:
            custom_command_entry = await CustomCommands._get_command_entry(name, session)
            if custom_command_entry:
                try:
                    valid_fields = {c.name for c in DbCc.__table__.columns}
                    updates = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}
                    for key, value in updates.items():
                        setattr(custom_command_entry, key, value)

                    session.add(custom_command_entry)
                    await session.commit()
                    return "The custom command was updated successfully."

                except SQLAlchemyError as e:
                    tb_str = traceback.format_exc()
                    await send_error("edit_custom_command", f"{str(e)}\n{tb_str}")
                    return "Something went wrong, please check error logs."
            return "No custom command was found."

    @staticmethod
    async def delete_custom_command(name: str) -> str:
        """Deletes a custom command from the database"""
        async with session_factory() as session:
            try:
                command_entry = await CustomCommands._get_command_entry(name, session)
                if command_entry:
                    await session.delete(command_entry)
                    await session.commit()
                    return "The custom command was deleted successfully."
                return "There was an error getting custom command."
            except SQLAlchemyError as e:
                tb_str = traceback.format_exc()
                await send_error("delete_custom_command", f"{str(e)}\n{tb_str}")
                if session.is_active:
                    await session.rollback()
                    logger.error("Database error while deleting custom command: %s\nRolling back....", e, exc_info=True)
                return "Something went wrong, please check error logs."
