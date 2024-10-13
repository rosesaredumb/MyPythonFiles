from logging import basicConfig
from settings import asyncio, commands, discord, json, os, app_commands
from functools import partial

class basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = './mindmap/data.json'


    async def send_embed_response(self, interaction: discord.Interaction, title: str = "", description: str = "", color: discord.Color = discord.Color.blue()):
        """
        Create and send an embed response.

        Args:
            interaction (discord.Interaction): The interaction to respond to.
            title (str): The title of the embed.
            description (str): The description of the embed.
            color (discord.Color): The color of the embed.
        """
        embed = discord.Embed(title=title, description=f"```\n{description}\n```", color=color)
        await interaction.response.send_message(embed=embed)
       
    @app_commands.command(name="test", description="k")
    async def test(self, interaction: discord.Interaction):
        """Testing command"""
        await self.send_embed_response(interaction, description="hi")

    @app_commands.command(name="add", description="Add two numbers.")
    @app_commands.describe(a="The first number.", b="The second number.")
    async def add(self, interaction: discord.Interaction, a: float, b: float):

        result = a + b
        await interaction.response.send_message(f"The result of {a} + {b} is {result}.")

    @app_commands.command(name="choose_color", description="Choose a color from the list.")  
    @app_commands.describe(color_choice="Select a color from the available options.")  
    @app_commands.choices(color_choice=[  
        app_commands.Choice(name="Red", value="red"),  
        app_commands.Choice(name="Green", value="green"),  
        app_commands.Choice(name="Blue", value="blue"),  
        app_commands.Choice(name="Yellow", value="yellow"),  
    ])  
    async def choose_color(self, interaction: discord.Interaction, color_choice: str):  
        await interaction.response.send_message(f"You chose the color: {color_choice}")

    

async def setup(bot):
    await bot.add_cog(basics(bot))
