# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""This file contains the error reporting logic"""
from typing import Dict, Optional
import os
from datetime import datetime as dt, timezone as tz
import aiohttp
import discord
from discord import Webhook, Embed
from discord.ui import View, Button
from dotenv import load_dotenv
from .logger import logger
load_dotenv()

url = os.getenv("MB_URL")
password = os.getenv("MB_PASSWORD")
headers = {"Content-Type": "application/json",
           "User-Agent": "CytanixBot/1.0 (Python AIOHTTP) Coded by Cytanix/SpiritTheWalf"}

class ErrorView(View): # type: ignore
    """Subclasses View for a custom view"""
    def __init__(self, message_id: int):
        super().__init__(timeout=None)
        self.message_id = message_id
        self.error_url: Optional[str] = None
        self.delete_url: Optional[str] = None

    @discord.ui.button(label="View Error", style=discord.ButtonStyle.green) # type: ignore
    async def view_error(self, interaction: discord.Interaction, button: Button) -> None: # pylint: disable=W0613
        """View Error Button"""
        await interaction.response.send_message(f"[View Error]({self.error_url})", ephemeral=True)

    @discord.ui.button(label="Delete Error", style=discord.ButtonStyle.danger) # type: ignore
    async def delete_error(self, interaction: discord.Interaction, button: Button) -> None: # pylint: disable=W0613
        """Delete Error Button"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}/api/security/delete/{self.delete_url}") as resp:
                response_text = await resp.text()

                if response_text.strip() == "Ok":
                    try:
                        self.stop()
                        await interaction.response.send_message("Error deleted successfully.", ephemeral=True)
                    except discord.NotFound:
                        await interaction.response.send_message("Error message not found.", ephemeral=True)
                else:
                    await interaction.response.send_message("Failed to verify deletion.", ephemeral=True)


async def send_error(name: str, error: str) -> Dict[str, str]:
    """This function sends the error report for the given name"""
    payload = {
        "Expires": None,
        "files": [{
            "content": error,
            "filename": name,}],
        "password": password,
    }
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(os.getenv('WEBHOOK_URL'), session=session)
        async with session.post(f"{url}/api/paste", json=payload, headers=headers) as response:
            if response.status != 200:
                logger.error("An error occurred while sending error report")
                await webhook.send("An error occurred while sending error report",
                                   username="Error Errored",
                                   avatar_url="https://media.tachyonind.org/h5MU")
                return {"Response": "An error occurred while sending error report"}

            data = await response.json()

            view = ErrorView(message_id=data["id"])
            view.error_url = f"{url}/api/paste/{data['id']}"
            view.delete_url = data["safety"]

            embed = Embed(title="New Error Report")
            embed.set_footer(text=dt.now(tz.utc).strftime("%m/%d/%Y %H:%M"))
            await webhook.send(embed=embed)

            return {"error_url": data["id"], "delete_url": data["safety"]}
