# This is ChatGPT Generated code, purely for testing purposes
"""This file tests the Punishment table functions"""
import asyncio
import traceback
from database.db_io import Punishments

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_punishments() -> None:
    """Function to test the Punishment table functions"""
    try:
        guild_id = 123456789
        user_id = 987654321

        # Test add_punishment
        punishment_data = {
            "guild_id": guild_id,
            "user_id": user_id,
            "punishment": "Ban",
            "punishment_time": 1712509200,  # Example UNIX timestamp
            "moderator_id": 123123123,
            "reason": "Breaking rules"
        }
        add_result = await Punishments.add_punishment(**punishment_data)
        print("Add Punishment:", add_result)

        # Fetch all punishments for the user
        user_punishments = await Punishments.get_punishments_by_user(user_id, guild_id)
        print(f"Punishments for user {user_id}:", user_punishments)

        # Get the last inserted punishment ID
        if isinstance(user_punishments, Punishments):
            last_punishment_id = user_punishments[-1].punishment_id
        else:
            print("No punishments found for user.")
            return

        # Get punishment with ID 1
        punishment_entry = await Punishments.get_punishment(1, guild_id)
        print("Punishment with ID 1:", punishment_entry)

        # Get the last added punishment
        last_punishment_entry = await Punishments.get_punishment(last_punishment_id, guild_id)
        print(f"Last added punishment (ID {last_punishment_id}):", last_punishment_entry)

    except Exception as e: # pylint: disable=W0718
        tb_str = traceback.format_exc()
        print(f"Test encountered an error: {str(e)}\n{tb_str}")

if __name__ == "__main__":
    asyncio.run(test_punishments())
