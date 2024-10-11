from settings import discord, commands, os, retrieve_keys

TOKEN = str(retrieve_keys("DISCORD_TOKEN"))
intents = discord.Intents.all()

# Initialize the bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Event when the bot is ready
async def load_extensions():
    for filename in os.listdir('./discord_bot/2024/cogs'):
        if filename.endswith('.py') and filename != "__init__.py":
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"Loaded {cog_name}")
            except Exception as e:
                print(f"Failed to load {cog_name}: {e}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await load_extensions()
    synced = await bot.tree.sync()  # Sync slash commands
    print(f"synced {len(synced)} command(s)")
    print("Slash commands synced.")

# Function to load all cogs from the 'cogs' folder

# Run the bot
if __name__ == "__main__":
    #bot.loop.run_until_complete(load_extensions())
    bot.run(TOKEN)