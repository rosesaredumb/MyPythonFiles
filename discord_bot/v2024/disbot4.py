from mymods import retrieve_keys, discord, commands

TOKEN = retrieve_keys("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents, application_id=1290060881740169236)


async def main():
    async with bot:
        await bot.load_extension('cogs')  # Load extensions before running the bot
        await bot.tree.sync()    # Sync the commands with Discord
        await bot.start(TOKEN)  # Start the bot

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
