"""This file is AI generated, purely for testing purposes"""
# mypy: disable-error-code=arg-type
import asyncio
from database.db_io import Registration
from utils import enums # Adjust import paths as needed

async def test_registration() -> None:
    """Function to test registration"""
    user_id = 1174000666012823565 # Use my ID here

    print("Registering user...")
    result = await Registration.register_new_user(
        user_id=user_id,
        gender=enums.Gender.MALE.value,
        sexuality=enums.Sexuality.STRAIGHT.value,
        position=enums.Position.SWITCH.value,
        dms=enums.Dms.ASK.value,
        relationship=enums.Relationship.SINGLE.value,
        mention=False,
        dob="01/01/1999"
    )
    print(result)

    print("Checking user entry...")
    user = await Registration.check_user_entry(user_id)
    print(f"User found: {user is not None}")

    print("Updating user entry...")
    update_result = await Registration.update_reg_entry(user_id, relationship=str(enums.Relationship.TAKEN))
    print(update_result)

    print("Deleting user entry...")
    delete_result = await Registration.delete_user_entry(user_id)
    print(delete_result)

    print("Checking user entry after deletion...")
    user_after_delete = await Registration.check_user_entry(user_id)
    print(f"User found: {user_after_delete is not None}")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_registration())
