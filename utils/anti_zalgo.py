# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""This file contains functions to detect and remove zalgo from usernames and text"""
import unicodedata
import asyncio

async def contains_zalgo(text: str) -> bool:
    """This function checks if the text contains zalgo"""
    return await asyncio.to_thread(
        lambda: any(unicodedata.combining(char) for char in text)
    )

async def cleanup_zalgo(text: str) -> str:
    """This function cleans up zalgo"""
    return await asyncio.to_thread(
        lambda: "".join(char for char in unicodedata.normalize("NFKC", text) if not unicodedata.combining(char))
    )
