"""THis file is AI generated, purely for testing purposes"""

import asyncio
from database.db_io import RegRoles  # Your logic class with setup/get/remove
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Replace these with real role IDs for testing or dummy values
TEST_GUILD_ID = 123456789
TEST_ROLE_DATA = {
    "registered": 1,
    "mention_mention": 2,
    "mention_no_mention": 3,
    "dms_allowed": 4,
    "dms_not_allowed": 5,
    "dms_ask": 6,
    "gender_male": 7,
    "gender_female": 8,
    "gender_genderfluid": 9,
    "gender_agender": 10,
    "gender_non_binary": 11,
    "gender_transgender": 12,
    "gender_trans_male": 13,
    "gender_trans_female": 14,
    "relationship_taken": 15,
    "relationship_single": 16,
    "relationship_single_seeking": 17,
    "relationship_single_not": 18,
    "relationship_rather_not": 19,
    "sexuality_asexual": 20,
    "sexuality_bisexual": 21,
    "sexuality_gay": 22,
    "sexuality_lesbian": 23,
    "sexuality_pansexual": 24,
    "sexuality_aromantic": 25,
    "sexuality_rather_not": 26,
    "position_dominant": 27,
    "position_submissive": 28,
    "position_switch": 29,
    "position_rather_not": 30,
    "position_neither": 31,
}


async def run_tests() -> None:
    """Function to run tests"""
    print("1. Testing setup_roles...")
    result = await RegRoles.setup_roles(TEST_GUILD_ID, **TEST_ROLE_DATA)
    print("→", result)
    assert "successfully" in result.lower()

    print("2. Testing get_roles...")
    entry = await RegRoles.get_roles(TEST_GUILD_ID)
    assert entry is not None, "No entry returned!"
    print("→ Got entry:", entry)
    assert entry.guild_id == TEST_GUILD_ID
    for key, value in TEST_ROLE_DATA.items():
        assert getattr(entry, key) == value, f"{key} does not match!"

    print("3. Testing remove_roles...")
    result = await RegRoles.remove_roles(TEST_GUILD_ID)
    print("→", result or "Roles removed successfully")
    entry = await RegRoles.get_roles(TEST_GUILD_ID)
    assert entry is None, "Entry still exists after removal!"

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    asyncio.run(run_tests())
