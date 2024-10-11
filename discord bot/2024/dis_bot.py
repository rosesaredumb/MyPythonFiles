import os
import json
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


with open('config.json') as config_file:
    config = json.load(config_file)
TOKEN = config.get('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'logged on as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)



@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    before = bot.latency
    await interaction.response.send_message(before)


@bot.tree.command(name="hlo")
async def hlo(interaction: discord.Interaction):
    await interaction.response.send_message("hi")


@bot.tree.command(name="serverinfo")
async def serverinfo(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(
            "This command can only be used in a server.")
        return  # Corrected indentation: using spaces instead of tabs
    guild = interaction.guild
    embed = discord.Embed(title="Server data",
                          colour=discord.Colour.blue(),
                          timestamp=interaction.created_at)
    embed.add_field(name="Server name", value=guild.name, inline=True)
    await interaction.response.send_message(embed=embed)


#token = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")
bot.run(TOKEN)
