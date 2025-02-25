from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv("DATABASE_URL")

async def test_connection():
    try:
        engine = create_async_engine(URL, echo=False)
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: print("Connected Successfully"))
        await engine.dispose()
    except Exception as e:
        print(e)

asyncio.run(test_connection())
