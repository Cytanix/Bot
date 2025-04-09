# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""Contains the functions to interact with the database"""
import traceback
from typing import Union, Any, cast, Optional, List
from datetime import datetime as dt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from utils.logger import logger
from utils.error_reporting import send_error
from utils import enums
from database.makedb import (
    session_factory,
    Logs as DbLog,
    Punishments as DbPunishments,
    CustomCommands as DbCc,
    Registration as DbReg,
    Levels as DbLvl,
    RegRoles as DbRr)


class Logs: # Checked and working, finalized
    """Defines the log structure"""

    @staticmethod
    async def _get_guild_entry(guild_id: int, session: AsyncSession) -> DbLog:
        """Helper method to get a guild entry"""
        result = await session.execute(select(DbLog).filter(DbLog.guild_id == guild_id))
        if result:
            return cast(DbLog, result.scalars().first())
        raise ValueError(f"No guild found with id {guild_id}")

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
                    raise ValueError(f"No guild found with id {guild_id}")
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


class Punishments: # Checked and working, finalized
    """Defines the punishment structure"""

    @staticmethod
    async def _get_punishment_entry(punishment_id: int, session: AsyncSession) -> DbPunishments:
        """Helper method to get a punishment entry"""
        result = await session.execute(select(DbPunishments).filter(DbPunishments.punishment_id == punishment_id))
        if result is not None:
            return cast(DbPunishments, result.scalars().first())
        raise ValueError(f"No punishment found with ID {punishment_id}")


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
    async def _get_command_entry(name: str, session: AsyncSession) -> Optional[DbCc]:
        """Helper method to get a command entry"""
        result = await session.execute(select(DbCc).filter(DbCc.name == name))
        entry = result.scalars().first()
        return entry if isinstance(entry, DbCc) else None

    @staticmethod
    async def add_custom_command(**kwargs: Any) -> str:
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


class Registration:
    """Defines the registration structure"""


    @staticmethod
    async def _get_reg_entry(user_id: int, session: AsyncSession) -> Optional[DbReg]:
        """Helper method to get a command entry"""
        result = await session.execute(select(DbReg).filter(DbReg.user_id == user_id))
        entry = result.scalars().first()
        return entry if isinstance(entry, DbReg) else None

    @staticmethod
    async def register_new_user( # pylint: disable=R0913,R0917
            user_id: int,
            gender: enums.Gender,
            sexuality: enums.Sexuality,
            position: enums.Position,
            dms: enums.Dms,
            relationship: enums.Relationship,
            mention: bool,
            dob: int,
    ) -> str:
        """Registers a new user"""
        async with session_factory() as session:
            try:
                user_entry = DbReg(
                    user_id=user_id,
                    gender=gender,
                    sexuality=sexuality,
                    position=position,
                    dms=dms,
                    relationship=relationship,
                    mention=mention,
                    dob=dob,
                    registered_at=dt.now().timestamp(),
                    age_verified=False,
                    artist_verified=False,
                    nsfw_lockout=False,
                    artist_lockout=False
                )
                session.add(user_entry)
                await session.commit()
                return "The user was registered successfully."

            except SQLAlchemyError as e:
                if session.is_active:
                    await session.rollback()
                logger.error("Database error while registering new user: %s\nRolling back....", e, exc_info=True)
                tb_str = traceback.format_exc()
                await send_error("register_new_user", f"{str(e)}\n{tb_str}")
                return "Something went wrong, please check error logs."

    @staticmethod
    async def update_reg_entry(user_id: int, **kwargs: Any) -> str:
        """Updates a registration entry"""
        async with session_factory() as session:
            user_entry = await Registration._get_reg_entry(user_id, session)
            if user_entry:
                try:
                    valid_fields = {c.name for c in DbReg.__table__.columns}
                    updates = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}
                    for key, value in updates.items():
                        setattr(user_entry, key, value)
                    await session.commit()
                    return "The registration entry was updated successfully."

                except SQLAlchemyError as e:
                    if session.is_active:
                        await session.rollback()
                    logger.error("Database error while updating registration entry: %s\nRolling back....", e, exc_info=True)
                    tb_str = traceback.format_exc()
                    await send_error("update_reg_entry", f"{str(e)}\n{tb_str}")
                    return "Something went wrong, please check error logs."
            return "No user found"

    @staticmethod
    async def check_user_entry(user_id: int) -> Optional[DbReg]:
        """Checks a registration entry"""
        async with session_factory() as session:
            result = await Registration._get_reg_entry(user_id, session)
        return result if result else None

    @staticmethod
    async def delete_user_entry(user_id: int) -> Optional[str]:
        """Deletes a registration entry"""
        async with session_factory() as session:
            try:
                result = await Registration._get_reg_entry(user_id, session)
                if result:
                    await session.delete(result)
                    await session.commit()
                    return "The user was deleted successfully."
                return None
            except SQLAlchemyError as e:
                if session.is_active:
                    await session.rollback()
                logger.error("Database error while updating registration entry: %s\nRolling back....", e, exc_info=True)
                tb_str = traceback.format_exc()
                await send_error("update_reg_entry", f"{str(e)}\n{tb_str}")
                return "Something went wrong, please check error logs."


class Levels:
    """Defines the Levels structure"""


    @staticmethod
    async def add_user_in_guild(guild_id: int, user_id: int) -> str:
        """Adds a user to a guild"""
        async with session_factory() as session:
            try:
                level_entry = DbLvl(
                    guild_id=guild_id,
                    user_id=user_id,
                )
                session.add(level_entry)
                await session.commit()
                return f"User with id {user_id} was added to guild {guild_id}."
            except SQLAlchemyError as e:
                if session.is_active:
                    session.rollback()
                logger.error("Database error while adding new user to guild: %s\nRolling back....", e, exc_info=True)
                tb_str = traceback.format_exc()
                await send_error("update_reg_entry", f"{str(e)}\n{tb_str}")
                return "Something went wrong, please check error logs."

    @staticmethod
    async def get_user_in_guild(guild_id: int, user_id: int) -> Union[DbLvl, str]:
        """Gets a user from a guild"""
        async with session_factory() as session:
            user_entry = (await session.execute(select(DbLvl).filter(DbLvl.guild_id == guild_id, DbLvl.user_id == user_id))).scalars().first()
            if user_entry:
                return cast(DbLvl, user_entry)
            return "No user found for that ID and guild"

    @staticmethod
    async def get_all_users_in_guild(guild_id: int) -> List[DbLvl]:
        """Gets all users from a guild"""
        async with session_factory() as session:
            users = (await session.execute(select(DbLvl).filter(DbLvl.guild_id == guild_id))).scalars().all()
            return cast(list[DbLvl], users)

    @staticmethod
    async def get_all_guilds() -> Optional[List[int]]:
        """Gets all unique guild IDs"""
        async with session_factory() as session:
            result = await session.execute(select(DbLvl.guild_id).distinct())
            guilds = list(result.scalars())
            return guilds if guilds else None

    @staticmethod
    async def get_all_users() -> Optional[List[int]]:
        """Gets all users"""
        async with session_factory() as session:
            result = await session.execute(select(DbLvl.user_id).distinct())
            users = list(result.scalars())
            return users if users else None

    @staticmethod
    async def add_xp(guild_id: int, user_id: int, xp: int) -> str:
        """Adds XP to a user."""
        async with session_factory() as session:
            try:
                user = (await session.execute(
                    select(DbLvl).filter(DbLvl.guild_id == guild_id, DbLvl.user_id == user_id))).scalars().first()
                if user:
                    user.xp += xp
                    await session.commit()
                    return "XP successfully added"
                return "No user found with that ID for that guild"
            except SQLAlchemyError as e:
                if session.is_active:
                    await session.rollback()
                logger.error("Database error while adding XP: %s\nRolling back....", e, exc_info=True)
                tb_str = traceback.format_exc()
                await send_error("add_xp", f"{str(e)}\n{tb_str}")
                return "Something went wrong, please check error logs."

    @staticmethod
    async def remove_xp(guild_id: int, user_id: int, xp: int) -> str:
        """Removes XP from a user."""
        async with session_factory() as session:
            try:
                user = (await session.execute(
                    select(DbLvl).filter(DbLvl.guild_id == guild_id, DbLvl.user_id == user_id))).scalars().first()
                if user:
                    user.xp -= xp
                    await session.commit()
                    return "XP successfully removed"
                return "No user found with that ID for that guild"
            except SQLAlchemyError as e:
                if session.is_active:
                    await session.rollback()
                logger.error("Database error while removing XP: %s\nRolling back....", e, exc_info=True)
                tb_str = traceback.format_exc()
                await send_error("remove_xp", f"{str(e)}\n{tb_str}")
                return "Something went wrong, please check error logs."

    @staticmethod
    async def remove_user_from_guild(guild_id: int, user_id: int) -> str:
        """Removes a user from a guild"""
        async with session_factory() as session:
            try:
                user = (await session.execute(
                    select(DbLvl).filter(DbLvl.guild_id == guild_id, DbLvl.user_id == user_id))).scalars().first()

                if user:
                    await session.delete(user)
                    await session.commit()
                    return "User deleted successfully."

                return "No user found with that ID for that guild."
            except SQLAlchemyError as e:
                if session.is_active:
                    await session.rollback()
                logger.error("Database error while removing user: %s\nRolling back....", e, exc_info=True)
                tb_str = traceback.format_exc()
                await send_error("remove_user_from_guild", f"{str(e)}\n{tb_str}")
                return "Something went wrong, please check error logs."


class RegRoles:
    """Defines the RegRoles structure"""

    @staticmethod
    async def setup_roles(guild_id: int, **kwargs: Any) -> str:
        """Adds the roles to the db"""
        try:
            async with session_factory() as session:
                reg_entry = DbRr(
                    guild_id=guild_id,
                    **kwargs
                )
                session.add(reg_entry)
                await session.commit()
                return "Roles successfully added."
        except SQLAlchemyError as e:
            if session.is_active:
                await session.rollback()
            logger.error("Database error while updating setting up registration roles: %s\nRolling back....", e, exc_info=True)
            tb_str = traceback.format_exc()
            await send_error("setup_roles", f"{str(e)}\n{tb_str}")
            return "Something went wrong, please check error logs."


    @staticmethod
    async def remove_roles(guild_id: int) -> str:
        """Removes the roles from the db"""
        try:
            async with session_factory() as session:
                entry = (await session.execute(select(DbRr).filter(DbRr.guild_id == guild_id))).scalars().first()
                if not entry:
                    return "No guild found with that ID"
                await session.delete(entry)
                await session.commit()
                return "Deletion successful."
        except SQLAlchemyError as e:
            if session.is_active:
                await session.rollback()
            logger.error("Database error while updating removing registration roles: %s\nRolling back....", e, exc_info=True)
            tb_str = traceback.format_exc()
            await send_error("remove_roles", f"{str(e)}\n{tb_str}")
            return "Something went wrong, please check error logs."

    @staticmethod
    async def get_roles(guild_id: int) -> Optional[List[int]]:
        """Gets and returns the roles from the db"""
        async with session_factory() as session:
            entry = (await session.execute(select(DbRr).filter(DbRr.guild_id == guild_id))).scalars().first()
            return entry if entry else None
