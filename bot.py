"""
This is the main file for the bot.
It contains the bot class and the main function to run the bot.
"""
import json
import os
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import ExtensionError
from dotenv import load_dotenv


load_dotenv()
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True


async def cog_loader(bot_instance: commands.Bot) -> None:
    """This function loads all cogs in the cogs folder plus jishaku."""
    await bot_instance.load_extension('jishaku')
    for file in os.listdir('cogs'):
        if file.endswith('.py') and file != '__init__.py':
            cog_name = file[:-3]
            try:
                await bot_instance.load_extension(f'cogs.{cog_name}')
                print(f'Successfully loaded {cog_name}')
            except  ExtensionError as e:
                print(f'Failed to load cog {cog_name}: {str(e)}')
                print(traceback.format_exc())

class Cytanix(commands.Bot):
    """This is the main bot class."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage = "Development"
        self.version = "0.0.1"
        self.session_command_count = 0
        self.command_count = self.load_command_count()  # Load saved count

    @staticmethod
    def load_command_count():
        file_path = "utils/command_count.json"  # Adjust the path

        # If the file does not exist, create it with default data
        if not os.path.exists(file_path):
            print("File not found. Creating new JSON file with count = 0.")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({"count": 0}, f, indent=2)
            return 0  # Return default count

        # If file exists but is empty, write default content
        if os.stat(file_path).st_size == 0:
            print("File is empty. Writing default content.")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({"count": 0}, f, indent=2)
            return 0

        # Try to load the JSON data
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f).get("count", 0)
        except json.JSONDecodeError:
            print("Invalid JSON detected. Resetting file.")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({"count": 0}, f, indent=2)
            return 0

    def save_command_count(self):
        """Saves the command count to a JSON file."""
        with open("utils/command_count.json", "w") as f:
            json.dump({"count": self.command_count}, f)

    async def on_command_completion(self, ctx):
        """Triggered when a command is used."""
        self.command_count += 1
        self.save_command_count()

    async def setup_hook(self) -> None:
        """This function is called before the bot is ready, to load cogs."""
        await cog_loader(self)

    async def on_ready(self):
        """This function is called when the bot is ready."""
        print(f'Logged in as {self.user.name}')
        print("Ready to recieve commands!")

bot = Cytanix(command_prefix=commands.when_mentioned_or("!"), intents=intents)

if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
