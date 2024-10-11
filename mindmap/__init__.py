from discord.ext import commands
import os

async def setup(bot: commands.Bot):
    """Load all cogs from the cogs directory."""
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}') 