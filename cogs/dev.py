# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""Contains Dev only commands"""
import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import aiohttp
load_dotenv()
portainer_api_key = os.getenv("PORTAINER_API_KEY")

headers = {"X-API-KEY": portainer_api_key}

@app_commands.allowed_contexts(guilds=True, dms=True)
class Dev(commands.GroupCog): # type: ignore
    """Cog that contains dev commands"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="pull") # type: ignore
    async def pull(self, inter: discord.Interaction) -> None:
        """Command to pull the latest changes from git"""
        await inter.response.defer()
        await inter.followup.send("Pulling changes...")

        process = await asyncio.create_subprocess_exec(
            "git", "pull",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() or stderr.decode().strip()
        await inter.followup.send(f"```\n{output}\n```")

        if "Already up to date." in output:
            await inter.followup.send("No updates found. Restart not required")
            return

        await inter.followup.send("Update successful. Restarting bot...")

        async with aiohttp.ClientSession() as session:
            async with session.post(url="https://portainer.cytanix.com/api/docker/3/containers/Cytanix/restart", headers=headers):
                pass # Bot is down, so no need to send message

async def setup(bot: commands.Bot) -> None:
    """Adds the cog to the bot"""
    await bot.add_cog(Dev(bot))
