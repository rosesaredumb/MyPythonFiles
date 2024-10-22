from discord_bot.v2024.cogs.mymodules import discord, commands, app_commands, ast, asyncio
from discord_bot.v2024.cogs.mymodules import send_embed_response, retrieve_keys, imgur_functions
import typing



class basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def images_autocomplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        xx = imgur_functions.get_imgur_album_images_with_descriptions(self)[1]
        for title_name in xx:
            if current.lower() in title_name.lower():
                data.append(app_commands.Choice(name=title_name, value=title_name))
        return data
       
    @app_commands.command(name="test", description="k")
    async def test(self, interaction: discord.Interaction):
        """Testing command"""
        x = imgur_functions.get_imgur_album_images_with_descriptions(self)[1]
        await send_embed_response(interaction, description=x)

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
    @app_commands.autocomplete(image_choice = images_autocomplete)
    async def images_command(self, interaction: discord.Interaction, image_choice: str):
        """
        Command to fetch and display images from an Imgur album.

        Args:
            interaction (discord.Interaction): The interaction to respond to.
            album_id (str): The ID of the Imgur album.
        """ 
        whole_data = imgur_functions.get_imgur_album_images_with_descriptions(self)[0]
        url_list = whole_data[image_choice]
        embeds = []
        num = 1
        for img_url in url_list:
            embed = discord.Embed(title=f"{image_choice} ({num})", color=discord.Color.blue())
            embed.set_image(url=img_url)
            embeds.append(embed)
            num += 1
        # Send embeds in batches if necessary
        await interaction.response.send_message(embeds=embeds[:10])
        if len(embeds) > 10:
            for batch_start in range(10, len(embeds), 10):
                await interaction.followup.send(embeds=embeds[batch_start:batch_start + 10])
    
    @app_commands.command(name="title", description="shows images from imgur album")
    async def title_command(self, interaction: discord.Interaction):
        """
        Command to fetch and display images from an Imgur album.

        Args:
            interaction (discord.Interaction): The interaction to respond to.
            album_id (str): The ID of the Imgur album.
        """ 
        qp_data = imgur_functions.get_imgur_album_images_with_descriptions(self)[0]
        qp = imgur_functions.get_imgur_album_images_with_descriptions(self)[1]

        found_keys = "\n".join([f"{i+1}: {key}" for i, key in enumerate(qp)])
        await send_embed_response(interaction, description=f"{found_keys}")

        def check(m):
                return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit()

        try:
            choice_msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            choice = int(choice_msg.content) - 1
            if 0 <= choice < len(qp):
                topic = qp[choice]
                url_list = qp_data[topic]
                embeds = []
                num = 1
                for img_url in url_list:
                    embed = discord.Embed(title=f"{topic} ({num})", color=discord.Color.blue())
                    embed.set_image(url=img_url)
                    embeds.append(embed)
                    num += 1
                # Send embeds in batches if necessary
                await interaction.followup.send(embeds=embeds[:10])
                if len(embeds) > 10:
                    for batch_start in range(10, len(embeds), 10):
                        await interaction.followup.send(embeds=embeds[batch_start:batch_start + 10])
        except asyncio.TimeoutError:
                await send_embed_response(interaction, description="Timeout! No response received.", type="followup")
        
        #whole_data = imgur_instance.get_imgur_album_images_with_descriptions()[0]
#
#
        #url_list = whole_data[album_id]
        #name = album_id
        #embeds = []
        #num = 1
        #for img_url in url_list:
        #    embed = discord.Embed(title=f"{name} ({num})", color=discord.Color.blue())
        #    embed.set_image(url=img_url)
        #    embeds.append(embed)
        #    num += 1
#
        ## Send embeds in batches if necessary
        #await interaction.response.send_message(embeds=embeds[:10])
        #if len(embeds) > 10:
        #    for batch_start in range(10, len(embeds), 10):
        #        await interaction.followup.send(embeds=embeds[batch_start:batch_start + 10])

async def setup(bot):
    await bot.add_cog(basics(bot))
