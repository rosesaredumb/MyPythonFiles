from mymods import *

TOKEN = retrieve_keys("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# File paths
file_path = './mindmap/data.json'

# Ensure the file exists or create it
if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        json.dump({"seed": {}}, f)
        print(f"{file_path} created!")
else:
    print(f"{file_path} already exists.")

# Helper functions for working with the JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def find_duplicate_keys(data, target_key, parent_path="", results=None):
    """
    Recursive function to find all identical keys in the JSON and their paths.
    """
    if results is None:
        results = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{parent_path}.{key}" if parent_path else key

            if key == target_key:
                # Store the current path and value of the matching key
                results.append((current_path, value))

            # Recursively check nested dictionaries
            if isinstance(value, dict):
                find_duplicate_keys(value, target_key, current_path, results)

    return results

async def update_key_value(data, path_to_update, new_value, ctx):
    current = data
    keys = path_to_update.split('.')
    for key in keys[:-1]:
        current = current[key]
    x = list(current[keys[-1]].keys())
    await ctx.send(f"Available keys: {x}")
    
    if new_value not in x:
        current[keys[-1]][new_value] = {}
    else:
        await ctx.send(f"That item already exists. Do you want to replace it? (yes/no)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            response = await bot.wait_for('message', check=check, timeout=60.0)
            if response.content.lower() in ['yes', 'y']:
                current[keys[-1]][new_value] = {}
                await ctx.send("Replaced.")
            else:
                await ctx.send("You chose not to continue.")
        except asyncio.TimeoutError:
            await ctx.send("Timeout! No response received.")

# Bot command to start the process
@bot.command(name="update_key")
async def update_key(ctx, target_key, *, new_value):
    """
    Command to find and update a key in the JSON file.
    Usage: !update_key key_name new_value
    """
    # Read the JSON file
    json_data = read_json(file_path)

    # Find duplicate keys in the JSON
    duplicate_keys = find_duplicate_keys(json_data, target_key)

    if len(duplicate_keys) > 1:
        await ctx.send(f"Found {len(duplicate_keys)} occurrences of the key '{target_key}':")
        for i, (path, value) in enumerate(duplicate_keys, start=1):
            await ctx.send(f"{i}: Path: {path}, Current Value: {value}")
        
        await ctx.send(f"Which '{target_key}' key would you like to update (1-{len(duplicate_keys)})?")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

        try:
            choice = await bot.wait_for('message', check=check, timeout=60.0)
            choice = int(choice.content) - 1
            if 0 <= choice < len(duplicate_keys):
                await update_key_value(json_data, duplicate_keys[choice][0], new_value, ctx)
            else:
                await ctx.send("Invalid choice.")
        except asyncio.TimeoutError:
            await ctx.send("Timeout! No response received.")
    elif len(duplicate_keys) == 1:
        await update_key_value(json_data, duplicate_keys[0][0], new_value, ctx)
    else:
        await ctx.send(f"No occurrences of the key '{target_key}' were found.")

    # Write updated data to the JSON file
    write_json(file_path, json_data)

# Run the bot
bot.run(TOKEN)