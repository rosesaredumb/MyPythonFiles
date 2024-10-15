from cogs.settings import discord, commands, app_commands, ast
from cogs.settings import send_embed_response, retrieve_keys, imgur_functions


imgur_instance = imgur_functions()
x = {}
imgur_album_IDs = ast.literal_eval(str(retrieve_keys("imgur album_IDs")))
for j in imgur_album_IDs:
    x[j] = imgur_instance.get_imgur_album_name(j)

image_choices = [app_commands.Choice(name=value, value=key) for key, value in x.items()]


class basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
       
    @app_commands.command(name="test", description="k")
    async def test(self, interaction: discord.Interaction):
        """Testing command"""
        await send_embed_response(interaction, description="hi")

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

    
    @app_commands.command(name="avatar", description="Get the enlarged avatar of a user.")
    async def avatar_command(self, interaction: discord.Interaction, user: discord.User):
        """
        Command to fetch and display the enlarged avatar of a specified user.

        Args:
            interaction (discord.Interaction): The interaction to respond to.
            user (discord.User, optional): The user whose avatar to fetch. Defaults to the command invoker.
        """
        # If no user is specified, use the command invoker
        user = user or interaction.user

        # Get the user's avatar URL (with the largest size)
        avatar_url = user.display_avatar.url
        # Create an embed with the avatar
        embed = discord.Embed(title=f"{user.name}'s Avatar", color=discord.Color.blue())
        embed.set_image(url=avatar_url)

        # Send the embed response
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="images", description="shows images from imgur album")
    @app_commands.choices(album_id = image_choices)
    async def images_command(self, interaction: discord.Interaction, album_id: str):
        """
        Command to fetch and display images from an Imgur album.

        Args:
            interaction (discord.Interaction): The interaction to respond to.
            album_id (str): The ID of the Imgur album.
        """ 
        imgur_images = imgur_functions.get_imgur_album_images(self, album_id)
        name = imgur_functions.get_imgur_album_name(self, album_id)
        embeds = []
        for img_url in imgur_images:
            embed = discord.Embed(title=name, color=discord.Color.blue())
            embed.set_image(url=img_url)
            embeds.append(embed)

        # Send embeds in batches if necessary
        await interaction.response.send_message(embeds=embeds[:10])
        if len(embeds) > 10:
            for batch_start in range(10, len(embeds), 10):
                await interaction.followup.send(embeds=embeds[batch_start:batch_start + 10])
    

async def setup(bot):
    await bot.add_cog(basics(bot))
