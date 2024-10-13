from mymods import retrieve_keys, commands, partial, discord

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    # Custom decorator for slash commands
    def slash_command(self, name: str, description: str):
        def decorator(func):
            async def wrapped_command(interaction: discord.Interaction):
                # Automatically pass interaction to the decorated function
                await func(interaction)
            self.tree.command(name=name, description=description)(wrapped_command)
            return func
        return decorator

    # Helper function to create an embed
    def create_embed(self, title: str = "", description: str = "", color: discord.Color = discord.Color.blue()) -> discord.Embed:
        return discord.Embed(title=title, description=description, color=color)

    # Helper function to send an embed response without manually passing interaction
    def send_embed_response(self, title: str, description: str, color: discord.Color = discord.Color.blue()):
        # We don't need to pass interaction anymore
        async def response_func(interaction: discord.Interaction):
            embed = self.create_embed(title=title, description=description, color=color)
            await interaction.response.send_message(embed=embed)
        return response_func

# Create an instance of your bot
bot = MyBot()

# Use the custom slash_command decorator
@bot.slash_command(name="hello", description="Responds with a hello message")
async def hello_command(interaction):
    await bot.send_embed_response(title="Hello!", description="This is an embedded response from the bot.")(interaction)

@bot.slash_command(name="info", description="Information about the bot")
async def info_command(interaction):
    await bot.send_embed_response(title="Bot Information", description="This bot is created using discord.py and sends all responses as embeds.")(interaction)

# Event to let us know the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync commands with Discord
    print(f'Logged in as {bot.user}!')

# Run the bot with your token
Token = str(retrieve_keys('DISCORD_TOKEN'))
bot.run(Token)