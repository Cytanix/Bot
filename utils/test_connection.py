# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""This file contains a combined test function for testing the connection and session query to the database."""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy import URL
from dotenv import load_dotenv
from database.makedb import session_factory, Logs, engine
import logging

load_dotenv()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

connection_url = URL.create(
    "postgresql+asyncpg",
    username=os.getenv("DATABASE_USERNAME"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    database=os.getenv("DATABASE"),
)


async def test_database() -> None:
    """Function to test both the connection to the database and a session query."""
    try:
        # Test the connection
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: logger.info("Connected Successfully"))

        # Test the session query
        async with session_factory() as session:
            result = await session.execute(select(Logs))
            logger.info("Session executed successfully.")
            logger.info(f"Query result: {result.all()}")
    except Exception as e:
        logger.error(f"Error during database tests: {e}")
    finally:
        await engine.dispose()


async def main():
    await test_database()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error running the main async event loop: {e}")
