# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""This file is chatgpt generated, purely for testing purposes"""
import asyncio
from typing import Any, Dict
from database.db_io import CustomCommands
from database.makedb import CustomCommands as DbCc

# Define a test command
test_command: Dict[str, Any]= {
    "name": "test_command",
    "owner_id": 123456789,
    "text": "This is a test command",
    "image": None,
    "nsfw": False
}


async def test_custom_commands() -> None:
    """Tests adding, retrieving, editing, and deleting a custom command."""

    # Add custom command
    add_result = await CustomCommands.add_custom_command(**test_command)
    print("Add Result:", add_result)

    retrieved_command = await CustomCommands.get_custom_command(test_command["name"])
    print("Retrieved Command:", retrieved_command)

    # Ensure retrieved_command is not None before accessing attributes
    assert retrieved_command is not None, "Failed to retrieve command"
    assert isinstance(retrieved_command, DbCc), "Unexpected type returned"
    assert retrieved_command.text == test_command["text"], "Text does not match"

    # Edit custom command
    edit_result = await CustomCommands.edit_custom_command(test_command["name"], text="Updated text")
    print("Edit Result:", edit_result)

    updated_command = await CustomCommands.get_custom_command(test_command["name"])

    if updated_command is None:
        raise ValueError("Failed to retrieve updated command, it may have been deleted or not exist.")

    assert updated_command.text == "Updated text", "Edit failed"

    # Delete custom command
    delete_result = await CustomCommands.delete_custom_command(test_command["name"])
    print("Delete Result:", delete_result)

    deleted_command = await CustomCommands.get_custom_command(test_command["name"])
    assert deleted_command is None, "Delete failed"

    print("All tests passed!")


if __name__ == "__main__":
    asyncio.run(test_custom_commands())
