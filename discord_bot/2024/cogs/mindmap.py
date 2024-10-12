from settings import asyncio, commands, discord, json, os, app_commands

class mindmap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = './mindmap/data.json'
        self.ensure_json_file()

    def ensure_json_file(self):
        """Ensure the JSON file exists or create it."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({"seed": {}}, f)
                print(f"{self.file_path} created!")
        else:
            print(f"{self.file_path} already exists.")

    # Helper functions for JSON handling
    def read_json(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def write_json(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

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

    def create_embed(self, title: str = "", description: str = "", color: discord.Color = discord.Color.blue()) -> discord.Embed:
        return discord.Embed(title=title, description=description, color=color)

    # Helper function to send an embed response
    async def send_embed_response(self, interaction: discord.Interaction, title: str = "", description: str = ""):
        embed = self.create_embed(title=title, description=f"```\n{description}\n```")
        await interaction.response.send_message(embed=embed)

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

    # Slash command to start the process
    @app_commands.command(name="update_key", description="Find and update a key in the JSON file")
    async def update_key(self, interaction: discord.Interaction, target_key: str, new_value: str):
        """
        Slash command to find and update a key in the JSON file.
        Usage: /update_key target_key new_value
        """
        # Read the JSON file
        json_data = self.read_json()

        # Find duplicate keys in the JSON
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
            await interaction.response.send_message(f"No occurrences of the key '{target_key}' were found.", ephemeral=True)

        # Write updated data to the JSON file
        self.write_json(json_data)

    @app_commands.command(name="skey")
    async def skey(self, interaction: discord.Interaction, target_key: str):
        json_data = self.read_json()

        # Find duplicate keys in the JSON
        duplicate_keys = self.find_keys(json_data, target_key)

        found_keys = "\n".join([f"{i+1}: {path}" for i, (path, value) in enumerate(duplicate_keys)])
        await self.send_embed_response(interaction, description=f"`{found_keys}`")
    


async def setup(bot):
    await bot.add_cog(mindmap(bot))
