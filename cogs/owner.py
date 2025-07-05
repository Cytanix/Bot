# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""Contains owner only commands"""
import asyncio
import os
import sys
import traceback
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import Cog, ExtensionFailed, Context
from utils.logger import logger
from utils.error_reporting import send_error
from database.db_io import BlacklistedUsers

class Owner(Cog): # type: ignore
    """Owner commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="sync", hidden=True) # type: ignore
    @commands.is_owner() # type: ignore
    async def sync(self, ctx: Context) -> None:
        """Command to sync the tree"""
        await self.bot.tree.sync()
        await ctx.send("Commands synced, you will need to reload Discord to see them.")
        await ctx.message.delete()
        logger.info("Commands synced")

    @commands.command(name="coglist", hidden=True) # type: ignore
    @commands.is_owner() # type: ignore
    async def coglist(self, ctx: Context) -> None:
        """List all loaded cogs"""
        loaded_cogs = "\n".join(self.bot.cogs.keys())
        await ctx.send(f"Loaded cogs:\n{loaded_cogs}")
        await ctx.message.delete()

    @commands.command(name="say", hidden=True)  # type: ignore
    @commands.is_owner()  # type: ignore
    async def say(self, ctx: Context, *, message: Optional[str] = None) -> None:
        """Make the bot say something"""
        attachments = ctx.message.attachments
        if message is None and not attachments:
            await ctx.send("You need to provide either a message or attachments")
            return
        try:
            files: list[bytes] = []
            if attachments:
                for attachment in attachments:
                    files.append(attachment.to_file())  # Fix append call
            if message:
                await ctx.send(message, files=files)  # Send message with attachments if present
            else:
                await ctx.send(files=files)  # Send only attachments if no message
        finally:
            await ctx.message.delete()  # Delete the original command message

    @commands.command(name="cutie", hidden=True) # type: ignore
    @commands.is_owner() # type: ignore
    async def cutie(self, ctx: Context, user: Optional[discord.Member] = None) -> None:
        """Everyone is a cutie, except me"""
        if user is None:
            user = ctx.author
        if user.id == 1174000666012823565:
            await ctx.send(f"{user.mention} is **not** a cutie!") # SpiritTheWalf
        elif user.id == 485213817958039573:
            await ctx.send(f"{user.mention} is...\n# THE CUTEST!!!") # NIIC
        else:
            await ctx.send(f"{user.mention} is a cutie!")

    @commands.command(name="presence", hidden=True) # type: ignore
    @commands.is_owner() # type: ignore
    async def presence(self, ctx: Context, *, status: discord.Status) -> None:
        """Set the presence"""
        if not isinstance(status, discord.Status):
            await ctx.send(f"Invalid status {status} please choose from: "
                           f"online, invisible, idle, do_not_disturb(dnd)")
        else:
            await self.bot.change_presence(status=status)
            await ctx.send(f"Bot status changed to {status}")
            await ctx.message.delete()
            logger.info("Bot status changed to %s", status)

    @commands.command(name="guild_info", hidden=True) # type: ignore
    @commands.is_owner() # type: ignore
    async def guild_info(self, ctx: Context, guild_id: Optional[int] = None) -> None:
        """Get information about a guild"""
        guild = self.bot.get_guild(guild_id if guild_id else ctx.guild.id)
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

    @commands.command(name="status", hidden=True) # type: ignore
    @commands.is_owner() # type: ignore # type: ignore
    async def status(self, ctx: Context, *, new_status: Optional[str] = None) -> None:
        """Change the bot's status"""
        if new_status is None:
            await self.bot.change_presence(activity=discord.Game(name=f"Patch {self.bot.version}"))
        else:
            await self.bot.change_presence(activity=discord.Game(name=new_status))
        await ctx.message.delete()
        logger.info("%s changed bot status", ctx.author)

    @commands.command(name='restart', hidden=True) # type: ignore
    @commands.is_owner() # type: ignore
    async def restart(self, ctx: Context) -> None:
        """Restart the bot"""
        await ctx.send('Restarting...')
        await self.bot.http.close()
        await self.bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command(name="killswitch", hidden=True) # type: ignore
    @commands.is_owner() # type: ignore
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

    @commands.command(name="reload", hidden=True) # type: ignore
    @commands.is_owner() # type: ignore
    async def reload(self, ctx: Context, cog: str) -> None:
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
            print(traceback.print_exception(type(e), e, e.__traceback__))
            await message.edit(content=f"Failed to reload {cog}:\n{e}")
        await ctx.message.delete()

    @commands.command(name="test_mb", hidden=True) # type: ignore
    async def test_mb(self, ctx: commands.Context) -> None:
        """Just a simple function to check if my error sending is working as intended"""
        error_name = "Test error"
        error_message = "This is a simulated error for testing purposes."
        result = await send_error(name=error_name, error=error_message)
        await ctx.message.add_reaction("✅")
        print(result)

    @commands.command(name="blacklist", hidden=True)
    @commands.is_owner()
    async def blacklist_add(self, ctx: commands.Context, user_id: int, *, reason: str) -> None:
        """Add a user to the blacklist"""
        response = await BlacklistedUsers.blacklist_user(user_id, reason=reason)
        await ctx.send(response)

    @commands.command(name="unblacklist", hidden=True)
    @commands.is_owner()
    async def unblacklist(self, ctx: commands.Context, user_id: int, *, reason: str) -> None:
        """Remove a user from the blacklist"""
        response = await BlacklistedUsers.remove_blacklisted_user(user_id, unblacklist_reason=reason)
        await ctx.send(response)

    @commands.command(name="checkblacklist", hidden=True)
    @commands.is_owner()
    async def checkblacklist(self, ctx: commands.Context, user_id: int) -> None:
        """Check if a user is blacklisted"""
        response = await BlacklistedUsers.get_blacklisted_user(user_id)
        if response:
            await ctx.send(f"User {user_id} has been blacklisted since "
                           f"{response.date_blacklisted} for reason: {response.reason}.")
        await ctx.send(f"User {user_id} is not in the blacklist.")

async def setup(bot: commands.Bot) -> None:
    """Setup function for Owner"""
    await bot.add_cog(Owner(bot))
