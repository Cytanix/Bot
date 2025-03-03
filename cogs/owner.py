# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""Contains owner only commands"""
import asyncio
import os
import sys
import traceback
from typing import Optional, TYPE_CHECKING
from datetime import datetime as dt
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Cog, ExtensionFailed, GuildNotFound, Context
from utils.logger import logger

if TYPE_CHECKING:
    from bot import Cytanix
    from discord.ext.commands import Context

class Owner(Cog):
    """Owner commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="sync", hidden=True)
    @commands.is_owner()
    async def sync(self, ctx: Context) -> None:
        """Command to sync the tree"""
        await self.bot.tree.sync()
        await ctx.send("Commands synced, you will need to reload Discord to see them.")
        await ctx.message.delete()
        logger.info("Commands synced")

    @commands.command(name="coglist", hidden=True)
    @commands.is_owner()
    async def coglist(self, ctx: Context) -> None:
        """List all loaded cogs"""
        loaded_cogs = "\n".join(self.bot.cogs.keys())
        await ctx.send(f"Loaded cogs:\n{loaded_cogs}")
        await ctx.message.delete()

    @commands.command(name="say", hidden=True)
    @commands.is_owner()
    async def say(self, ctx: Context, *, message: Optional[str] = None) -> None:
        """Make the bot say something"""
        attachments = ctx.message.attachments
        if message is None and not attachments:
            await ctx.send("You need to provide either a message or attachments")
            return
        try:
            if attachments:
                files = []
                for attachment in attachments:
                    files.append = attachment.to_file()
                    if message:
                        await ctx.send(message, files=files)
                    else:
                        await ctx.send(files=files)
            else:
                await ctx.send(message)
        finally:
            await ctx.message.delete()

    @commands.command(name="cutie", hidden=True)
    @commands.is_owner()
    async def cutie(self, ctx: Context, user: Optional[discord.Member] = None) -> None:
        """Everyone is a cutie, except me"""
        if user is None:
            user = ctx.author
        if user.id == 1174000666012823565:
            await ctx.send(f"{user.mention} is **not** a cutie!") # SpiritTheWalf
        elif user.id == 485213817958039573:
            await ctx.send(f"{user.mention} is...\n# THE CUTEST!!!") # NIIC
        elif user.id == 1186324527932776458:
            await ctx.send(f"{user.mention} is definitely an adorable cutie foxo!!!") # Mocha.The.Fox
        else:
            await ctx.send(f"{user.mention} is a cutie!")

    @commands.command(name="presence", hidden=True)
    @commands.is_owner()
    async def presence(self, ctx: Context, *, status: discord.Status) -> None:
        """Set the presence"""
        if not isinstance(status, discord.Status):
            await ctx.send(f"Invalid status {status} please choose from: "
                           f"online, invisible, idle, do_not_disturb(dnd)")
        else:
            await self.bot.change_presence(status=status)
            await ctx.send(f"Bot status changed to {status}")
            await ctx.message.delete()
            logger.info(f"Bot status changed to {status}")

    @commands.command(name="guild_info", hidden=True)
    @commands.is_owner()
    async def guild_info(self, ctx: Context, guild_id: Optional[int] = None) -> None:
        """Get information about a guild"""
        if guild_id is None:
            guild_id: discord.Guild.id = ctx.guild.id

        guild = self.bot.get_guild(guild_id)
        if guild is not None:
            embed = discord.Embed(
               title=f"Information for {guild.name}",
                colour= discord.Colour.from_str("#1010D1")
            )
            embed.add_field(name="Owner", value=f"{guild.owner}")
            embed.set_thumbnail(url=guild.icon.url)
            embed.add_field(name="Members", value=f"{guild.member_count}")
            embed.add_field(name="Text Channels", value=len(guild.text_channels))
            embed.add_field(name="Voice Channels", value=len(guild.voice_channels))
            embed.add_field(name="Created at",
            value=f"{guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            f" | {discord.utils.format_dt(guild.created_at, 'R')}")
            embed.add_field(
                name="Bot Joined At",
                value=guild.get_member(self.bot.user.id).joined_at.strftime('%Y-%m-%d %H:%M:%S'))
            embed.add_field(name="NSFW Level", value=guild.nsfw_level)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Guild not found, please try again later.\n"
                           "If error persists, please DM SpiritTheWalf.")

    @commands.command(name="status", hidden=True)
    @commands.is_owner()
    async def status(self, ctx: Context, *, new_status: Optional[str] = None) -> None:
        """Change the bot's status"""
        if new_status is None:
            await self.bot.change_presence(activity=discord.Game(name=f"Patch {self.bot.version}"))
        else:
            await self.bot.change_presence(activity=discord.Game(name=new_status))
        await ctx.message.delete()
        logger.info("%s changed bot status", ctx.author)

    @commands.command(name='restart', hidden=True)
    @commands.is_owner()
    async def restart(self, ctx: Context) -> None:
        """Restart the bot"""
        await ctx.send('Restarting...')
        await self.bot.http.close()
        await self.bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command(name="killswitch", hidden=True)
    @commands.is_owner()
    async def killswitch(self, ctx: Context, password: Optional[str] = None) -> None:
        """Stop the bot"""
        correct_password = "ThisIsAVerySecurePassword"

        if password is None:
            await ctx.send("Password required")
            await ctx.message.delete()
        elif password == correct_password:
            await ctx.send("Killswitch... ENGAGE!")
            await self.bot.close()

        else:
            await ctx.send("Wrong Password!")
            await ctx.message.delete()

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: Context, cog) -> None:
        """Reload a cog"""
        message = await ctx.send(f"Reloading {cog}")
        try:
            if cog in self.bot.extensions:
                await self.bot.reload_extension(cog)
                await asyncio.sleep(5)  # Adjust sleep time as needed
                await message.edit(content=f"Reloaded {cog} successfully!")
            else:
                await ctx.send(f"Cog {cog} not found")
        except ExtensionFailed as e:
            print(f"An error occurred while reloading extension: {e}")
            print(traceback.print_exc())
            await message.edit(content=f"Failed to reload {cog}:\n{e}")
        await ctx.message.delete()

async def setup(bot) -> None:
    """Setup function for Owner"""
    await bot.add_cog(Owner(bot))
