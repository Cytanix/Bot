# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
import json
import discord
from discord import app_commands
from discord.ext import commands

from utils.errors import NSFWEndpointCalled
from utils.redis import is_user_blacklisted


with open("utils/endpoints.json", "r", encoding="utf-8") as f:
    endpoints = json.load(f)

sfw_endpoints = endpoints["SFW_ENDPOINTS"]
nsfw_endpoints = endpoints["NSFW_ENDPOINTS"]

async def nsfw_endpoint(endpoint: str) -> bool:
    if endpoint in nsfw_endpoints:
        raise NSFWEndpointCalled()
    return False

def app_not_blacklisted():
    async def predicate(interaction: discord.Interaction) -> bool:
        return not await is_user_blacklisted(interaction.user.id)
    return app_commands.check(predicate)

def prefix_not_blacklisted():
    async def predicate(ctx):
        return not await is_user_blacklisted(ctx.author.id)
    return commands.check(predicate)