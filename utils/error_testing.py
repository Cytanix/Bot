# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""This file is just temporary for testing my webhook and api mechanics"""
import asyncio
from utils.error_reporting import send_error

async def test_error_reporting() -> None:
    """See above docstring"""
    error_name = "test_error"
    error_message = "This is a test error message."
    result = await send_error(error_name, error_message)
    print(result)


asyncio.run(test_error_reporting())
