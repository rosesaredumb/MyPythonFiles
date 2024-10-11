from settings import *

TOKEN = retrieve_keys("DISCORD_TOKEN")
intents = discord.Intents.default()

# Initialize the bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()  # Sync slash commands
    print("Slash commands synced.")

# Function to load all cogs from the 'cogs' folder
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Run the bot
if __name__ == "__main__":
    bot.loop.run_until_complete(load_extensions())
    bot.run('YOUR_DISCORD_BOT_TOKEN')