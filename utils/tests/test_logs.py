# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
# This is ChatGPT Generated code, purely for testing purposes
"""This file contains the functions to test the Logs table"""
import logging
import traceback
import asyncio
from sqlalchemy.exc import SQLAlchemyError
from database.db_io import Logs as LogsFunc
from database.makedb import session_factory, Logs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_logs_operations() -> None:
    """Function to test the logs operations"""
    guild_id = 514170870202368000  # Real guild ID for testing

    try:
        result = await LogsFunc.add_guild_on_join(guild_id)
        logger.info(result)

        guild = await LogsFunc.get_guild(guild_id)
        if isinstance(guild, str):
            logger.error("Error fetching guild: %s", guild)
        elif guild is None:
            logger.error("Guild is None, failed to fetch.")
        else:
            logger.info("Guild fetched successfully: %s", guild.guild_id)

        update_result = await LogsFunc.update_guild(guild_id, message_logs=100)
        logger.info(update_result)

        updated_guild = await LogsFunc.get_guild(guild_id)
        if isinstance(updated_guild, Logs):
            logger.info("Updated guild entry: %s", updated_guild.message_logs)
        elif updated_guild is None:
            logger.error("Guild is None, failed to update.")
        else:
            logger.error("Guild not found after update.")

        remove_result = await LogsFunc.remove_guild(guild_id)
        logger.info(remove_result)

        deleted_guild = await LogsFunc.get_guild(guild_id)
        if deleted_guild is None:
            logger.info("Guild %s successfully removed from the database.", guild_id)
        else:
            logger.error("Guild %s still exists in the database.", guild_id)

    except SQLAlchemyError as e:
        tb_str = traceback.format_exc()
        logger.error("Database error during operation: %s",  f'{e}\n{tb_str}')
    except Exception as e:  # pylint: disable=W0718
        logger.error("Unexpected error occurred: %s", str(e))
        logger.error("Exception type: %s", type(e))
        logger.error("Traceback details: %s", traceback.format_exc())

async def test_session() -> None:
    """Function to test the session"""
    async with session_factory() as session:
        print(f"Session created: {session}")



if __name__ == "__main__":
    asyncio.run(test_logs_operations())
