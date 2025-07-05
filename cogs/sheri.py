# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""Cog for fetching and displaying images from the Sheri API"""
import json
import os
import discord
import aiohttp
from typing import List, TYPE_CHECKING, Optional
from aiohttp import ClientConnectorError, ClientConnectionError
from dotenv import load_dotenv
from discord.ext.commands import GroupCog
from discord.app_commands import command, Choice, check, describe
from discord.ext import commands
import utils.errors
from utils.checks import app_not_blacklisted, nsfw_endpoint
from utils.error_reporting import send_error
from utils.errors import NSFWEndpointCalled

if TYPE_CHECKING:
    from bot import Cynix

load_dotenv()

with open("utils/endpoints.json", "r", encoding="utf-8") as f:
    endpoints = json.load(f)

sfw_endpoints = endpoints["SFW_ENDPOINTS"]


headers = {"Authorization": f"Token {os.getenv('API_KEY')}",
              "User-Agent": "CynixDev/0.1 (Python AIOHTTP) Coded by SpiritTheWalf" }

def extract_numbers(url: str) -> Optional[str]:
    parts = url.rstrip("/").split("/")
    if parts and parts[-1].isdigit():
        return parts[-1]
    return None

async def fetch_from_api(endpoint: str, count: int = 1):
    """Fetches data from the Sheri API"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"https://sheri.bot/api/{endpoint}?count={count}", headers=headers
        ) as response:

            if response.status == 200:
                data = await response.json()

                if isinstance(data, dict):
                    data = [data]

                image = data[0]

                image_url = image.get("url")
                report_url = image.get("report_url")
                author = image.get("author", {})
                artist_name = author.get("name", "Unknown")
                artist_link = author.get("link", "#")
                image_id = extract_numbers(report_url)
                footer_text = f"ID: {image_id} | Powered by the Sheri API"
                artist_text = f"[🎨 Artist: {artist_name}]({artist_link})"
                direct_url_text = f"[🌐 Direct URL to image]({image_url})"
                report_text = f"[Report to the Sheri Devs]({report_url})"

                embed = discord.Embed(title=f"{endpoint}")
                embed.set_image(url=image_url)
                embed.add_field(
                    name="",
                    value=f"{direct_url_text}\n{artist_text}\n{report_text}",
                )
                embed.set_footer(text=footer_text)
                return embed

            elif response.status == 401:
                raise utils.errors.UnauthorizedError()
            else:
                raise ClientConnectionError(
                    f"API request failed with error code {response.status}"
                )


class Sheri(GroupCog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="image", description="Get a (SFW) image from the Sheri API")
    @app_not_blacklisted()
    @describe(endpoint="The endpoint to call from")
    async def image(self, inter: discord.Interaction, endpoint: str):
        await inter.response.defer(thinking=True)
        try:
            nsfw = await nsfw_endpoint(endpoint)
        except NSFWEndpointCalled as e:
            await inter.followup.send(str(e), ephemeral=True)
            return

        message = await fetch_from_api(endpoint)
        await inter.followup.send(embed=message)

    @image.autocomplete("endpoint")
    async def image_autocomplete(self, inter: discord.Interaction, current: str) -> List[Choice[str]]:
        try:
            return [Choice(name=endpoint, value=endpoint) for endpoint in
                    sfw_endpoints if current.lower() in endpoint.lower()][:25]
        except Exception as e:
            print(e)
            await send_error("sheri_image", e)

async def setup(bot):
    await bot.add_cog(Sheri(bot))
