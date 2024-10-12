from logging import basicConfig
from settings import asyncio, commands, discord, json, os, app_commands
from functools import partial

class basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = './mindmap/data.json'


    def create_embed(self, title: str = "", description: str = "", color: discord.Color = discord.Color.blue()) -> discord.Embed:
        return discord.Embed(title=title, description=description, color=color)

    # Helper function to send an embed response
    async def send_embed_response(self, interaction: discord.Interaction, title: str = "", description: str = ""):
        embed = self.create_embed(title=title, description=f"```\n{description}\n```")
        await interaction.response.send_message(embed=embed)

       
    @app_commands.command(name="test", description="k")
    async def test(self, interaction: discord.Interaction):
        await self.send_embed_response(interaction, description="hi")
    

async def setup(bot):
    await bot.add_cog(basics(bot))
