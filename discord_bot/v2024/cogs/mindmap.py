from settings import asyncio, discord, commands, app_commands
from settings import send_embed_response, read_json, write_json, ensure_json_file
from settings import mindmap_json_path


class mindmap(commands.GroupCog, 
              group_name = "mmap", 
              group_description = "ff"):
    def __init__(self, bot):
        self.bot = bot
        ensure_json_file(mindmap_json_path)

    def find_keys(self, data, target_key, parent_path="", results=None):
        """
        Recursive function to find all identical keys in the JSON and their paths.
        """
        if results is None:
            results = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{parent_path}.{key}" if parent_path else key

                if key == target_key:
                    results.append((current_path, value))

                if isinstance(value, dict):
                    self.find_keys(value, target_key, current_path, results)

        return results

    async def update_key_value(self, data, path_to_update, new_value, interaction):
        current = data
        keys = path_to_update.split('.')
        for key in keys[:-1]:
            current = current[key]

        x = list(current[keys[-1]].keys())
        await interaction.response.send_message(f"Available keys: {x}", ephemeral=True)

        if new_value not in x:
            current[keys[-1]][new_value] = {}
        else:
            await interaction.followup.send("That item already exists. Do you want to replace it? (yes/no)", ephemeral=True)

            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel

            try:
                response = await self.bot.wait_for('message', check=check, timeout=60.0)
                if response.content.lower() in ['yes', 'y']:
                    current[keys[-1]][new_value] = {}
                    await interaction.followup.send("Replaced.", ephemeral=True)
                else:
                    await interaction.followup.send("You chose not to continue.", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("Timeout! No response received.", ephemeral=True)

    #@app_commands.command(name=)

    @app_commands.command(name="update", 
                          description="Find and update a key in the JSON file")
    @app_commands.describe(target_key = "The item you want to choose.", 
                           new_value = "The new value to create for that item.") 
    async def update(self, 
                     interaction: discord.Interaction, 
                     target_key: str, 
                     new_value: str):
        json_data = read_json(mindmap_json_path)
        duplicate_keys = self.find_keys(json_data, target_key)

        if len(duplicate_keys) > 1:
            found_keys = "\n".join([f"{i+1}: Path: {path}, Current Value: {value}" for i, (path, value) in enumerate(duplicate_keys)])
            await interaction.response.send_message(f"Found {len(duplicate_keys)} occurrences of the key '{target_key}':\n{found_keys}\nPlease choose one to update.", ephemeral=True)

            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit()

            try:
                choice_msg = await self.bot.wait_for('message', check=check, timeout=60.0)
                choice = int(choice_msg.content) - 1
                if 0 <= choice < len(duplicate_keys):
                    await self.update_key_value(json_data, duplicate_keys[choice][0], new_value, interaction)
                else:
                    await interaction.followup.send("Invalid choice.", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("Timeout! No response received.", ephemeral=True)
        elif len(duplicate_keys) == 1:
            await self.update_key_value(json_data, duplicate_keys[0][0], new_value, interaction)
        else:
            await send_embed_response(interaction, description=f"No occurrences of the key '{target_key}' were found.", ephemeral=True)

        write_json(json_data, mindmap_json_path)


    @app_commands.command(name = "show", 
                          description = "shows the item path")
    async def show(self, 
                   interaction: discord.Interaction, 
                   target_key: str):
        json_data = read_json(mindmap_json_path)
        duplicate_keys = self.find_keys(json_data, target_key)

        found_keys = "\n".join([f"{i+1}: {path}" for i, (path, value) in enumerate(duplicate_keys)])
        await send_embed_response(interaction, description=f"{found_keys}")
    

async def setup(bot):
    await bot.add_cog(mindmap(bot))