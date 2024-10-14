from settings import commands, os, traceback, logging, retrieve_keys, cogs_path, discord


TOKEN = retrieve_keys("discord rose_bot token")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def load_extensions():
    for filename in os.listdir(cogs_path):
        if filename.endswith('.py') and filename != "__init__.py":
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                logging.info(f'Loaded cog: {cog_name}')
                print(f"Loaded {cog_name}")
            except Exception as e:
                tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
                #logging.error(f'Failed to load cog {cog_name}: {tb_str}')
                print(f"Failed to load {cog_name}: {e}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        await load_extensions()
    except Exception as e:
        print(e)
    synced = await bot.tree.sync()
    print(synced)
    # Prepare to list commands and subcommands
    command_list = []
    
    for command in synced:
        # Add main command
        command_list.append(command.name)

        # Check if the command is a group (i.e., has subcommands)
        if isinstance(command, discord.app_commands.Group):
            for subcommand in command.commands:
                # Add subcommand (formatted as maincommand subcommand)
                command_list.append(f"{command.name} {subcommand.name}")

    # Print synced commands and subcommands
    print(f"synced {len(synced)} command(s)\n" + "\n".join(command_list))
    print("Slash commands synced.")


#@bot.event
#async def on_command_error(ctx, error):
#    # Log the full traceback
#    tb_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
#    logging.error(f'An error occurred: {tb_str}')
#
#    # Optionally, you can send a message to the user
#    await ctx.send(f'An error occurred: {str(error)}')

# Run the bot
if __name__ == "__main__":
    #bot.loop.run_until_complete(load_extensions())
    bot.run(TOKEN)