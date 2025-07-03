# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""This file contains the error reporting logic"""
from typing import Dict, Optional
import os
from datetime import datetime as dt, timezone as tz
import aiohttp
from discord import Webhook, Embed
from discord.ui import View, Button
from dotenv import load_dotenv
from bot import bot
from .logger import logger
load_dotenv()

url = os.getenv("MB_URL")
password = os.getenv("MB_PASSWORD")
headers = {"Content-Type": "application/json",
           "User-Agent": "CynixBot/1.0 (Python AIOHTTP) Coded by Cytanix/SpiritTheWalf"}

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
        webhook = Webhook.from_url(os.getenv('WEBHOOK_URL'), session=session, client=bot)
        async with session.post(f"{url}/api/paste", json=payload, headers=headers) as response:

            if response.status != 200:
                logger.error("An error occurred while sending error report")

                await webhook.send(content="An error occurred while sending error report",
                                   username="Error Errored",
                                   avatar_url="https://media.tachyonind.org/h5MU")
                return {"Response": "An error occurred while sending error report"}

            data = await response.json()

            view = ErrorView(error_url=f"{url}/{data['id']}",
                             delete_url = f"{url}/api/security/delete/{data['safety']}")
            bot.add_view(view)

            embed = Embed(title="New Error Report")
            embed.set_footer(text=dt.now(tz.utc).strftime("%m/%d/%Y %H:%M"))
            await webhook.send(embed=embed,
                               view=view,
                               username="New Error Report",
                               avatar_url="https://media.tachyonind.org/h5MU")

            return {"error_url": data["id"], "delete_url": data["safety"]}

class ErrorView(View):  # type: ignore
    """Custom error-handling view with unique delete button IDs"""
    def __init__(self, error_url: Optional[str] = None, delete_url: Optional[str] = None) -> None:
        super().__init__(timeout=None)

        self.error_url: Optional[str] = error_url
        self.delete_url: Optional[str] = delete_url

        if self.error_url:
            self.add_item(Button(label="View Error", url=self.error_url))

        if self.delete_url:
            self.add_item(Button(label="Delete Error", url=self.delete_url))
