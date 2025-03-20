# This is ChatGPT Generated code, purely for testing purposes
import logging
from database.db_io import Logs as LogsFunc
from sqlalchemy.exc import SQLAlchemyError
import traceback
import asyncio
from database.makedb import session_factory

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_logs_operations():
    guild_id = 514170870202368000  # Real guild ID for testing

    try:
        result = await LogsFunc.add_guild_on_join(guild_id)
        logger.info(result)

        guild = await LogsFunc.get_guild(guild_id)
        if isinstance(guild, str):
            logger.error(f"Error fetching guild: {guild}")
        else:
            logger.info(f"Guild fetched successfully: {guild.guild_id}")

        update_result = await LogsFunc.update_guild(guild_id, message_logs=100)
        logger.info(update_result)

        updated_guild = await LogsFunc.get_guild(guild_id)
        if updated_guild:
            logger.info(f"Updated guild entry: {updated_guild.message_logs}")
        else:
            logger.error("Guild not found after update.")

        remove_result = await LogsFunc.remove_guild(guild_id)
        logger.info(remove_result)

        deleted_guild = await LogsFunc.get_guild(guild_id)
        if deleted_guild is None:
            logger.info(f"Guild {guild_id} successfully removed from the database.")
        else:
            logger.error(f"Guild {guild_id} still exists in the database.")

    except SQLAlchemyError as e:
        tb_str = traceback.format_exc()
        logger.error(f"Database error during operation: {e}\n{tb_str}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Traceback details:\n{traceback.format_exc()}")

async def test_session():
    async with session_factory() as session:
        print(f"Session created: {session}")



if __name__ == "__main__":
    asyncio.run(test_logs_operations())
