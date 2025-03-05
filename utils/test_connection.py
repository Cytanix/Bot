# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""This file contains a function to test the connection to the database"""
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv("DATABASE_URL")

async def test_connection() -> None:
    try:
        engine = create_async_engine(URL, echo=False)
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: print("Connected Successfully"))
        await engine.dispose()
    except Exception as e:
        print(e)

asyncio.run(test_connection())
