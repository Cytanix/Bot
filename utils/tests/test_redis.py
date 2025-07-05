# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
import os
import asyncio
from dotenv import load_dotenv
import redis.asyncio as redis

load_dotenv()

async def main():
    r = redis.Redis(
        host=os.getenv("DATABASE_HOST"),
        port=6379,
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )

    pong = await r.ping()
    print("Connected!" if pong else "Failed to connect.")

    await r.set("foo", "bar")
    value = await r.get("foo")
    print(value)

    await r.aclose()

asyncio.run(main())
