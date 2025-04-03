"""This file is AI generated, purely for testing purposes"""
import asyncio
from typing import Any, Dict
from database.db_io import Levels
from database.makedb import Levels as DbLvl
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Define a test user and guild
TEST_GUILD_ID = 123456789
TEST_USER_ID = 987654321
TEST_XP = 100

test_entry: Dict[str, Any] = {
    "guild_id": TEST_GUILD_ID,
    "user_id": TEST_USER_ID
}

async def test_levels() -> None:
    """Tests adding a user, retrieving them, adding XP, and removing XP."""

    # Add user to guild
    add_result = await Levels.add_user_in_guild(**test_entry)
    print("Add Result:", add_result)

    retrieved_user = await Levels.get_user_in_guild(TEST_GUILD_ID, TEST_USER_ID)
    print("Retrieved User:", retrieved_user)

    assert isinstance(retrieved_user, DbLvl), "Unexpected type returned"
    assert retrieved_user.guild_id == TEST_GUILD_ID, "Guild ID does not match"
    assert retrieved_user.user_id == TEST_USER_ID, "User ID does not match"

    # Add XP
    add_xp_result = await Levels.add_xp(TEST_GUILD_ID, TEST_USER_ID, TEST_XP)
    print("Add XP Result:", add_xp_result)

    updated_user = await Levels.get_user_in_guild(TEST_GUILD_ID, TEST_USER_ID)
    if isinstance(updated_user, DbLvl):
        assert updated_user.xp == TEST_XP, "XP addition failed"
    print(f"updated user not expected type DbLvl, instead got {type(updated_user)}")

    # Remove XP
    remove_xp_result = await Levels.remove_xp(TEST_GUILD_ID, TEST_USER_ID, TEST_XP)
    print("Remove XP Result:", remove_xp_result)

    final_user = await Levels.get_user_in_guild(TEST_GUILD_ID, TEST_USER_ID)
    if isinstance(final_user, DbLvl):
        assert final_user.xp == 0, "XP removal failed"
    print(f"Final user not expected type DbLvl, instead got {type(final_user)}")

    # Get all users in guild
    all_users = await Levels.get_all_users_in_guild(TEST_GUILD_ID)
    print("All Users in Guild:", all_users)
    assert any(user.user_id == TEST_USER_ID for user in all_users), "User not found in guild list"

    woof = await Levels.remove_user_from_guild(TEST_GUILD_ID, TEST_USER_ID)
    print(woof)

    print("All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_levels())
