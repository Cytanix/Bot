# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
import os
import redis.asyncio as redis
from dotenv import load_dotenv
load_dotenv()

REDIS_BLACKLIST_SET = "blacklist_users"
_redis_client = None

async def get_redis() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(
            host=os.getenv("DATABASE_HOST"),
            port=6379,
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )
        try:
            await _redis_client.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}")
            raise
    return _redis_client

async def close_redis() -> None:
    global _redis_client
    if _redis_client:
        await _redis_client.flushdb()
        await _redis_client.aclose()
        _redis_client = None


async def load_blacklist_from_db(user_dicts: list[dict]):
    """Takes a list of user dicts (from DB) and loads user_ids into Redis."""
    redis_client = await get_redis()
    user_ids = [user["user_id"] for user in user_dicts if "user_id" in user]
    if user_ids:
        await redis_client.sadd(REDIS_BLACKLIST_SET, *user_ids)
        
async def is_user_blacklisted(user_id: int) -> bool:
    redis_client = await get_redis()
    return await redis_client.sismember(REDIS_BLACKLIST_SET, user_id)

async def blacklist_user_redis(user_id: int):
    redis_client = await get_redis()
    await redis_client.sadd(REDIS_BLACKLIST_SET, user_id)

async def remove_user_redis(user_id: int):
    redis_client = await get_redis()
    await redis_client.srem(REDIS_BLACKLIST_SET, user_id)