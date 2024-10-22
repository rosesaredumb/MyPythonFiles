import requests

from discord_bot.v2024.mymodules import retrieve_keys

# Replace this with your actual Imgur Client ID

ALBUM_ID = "ZXvh34o"  # The album ID you want to fetch
token = str(retrieve_keys("imgur client_ID"))
album_IDs = ["d9OwJIB", "3vYdMJL", "JXDIAKY"]

def get_imgur_album_images(album_id):
    # Imgur API endpoint to get album images
    url = f"https://api.imgur.com/3/album/{album_id}/images"

    # Imgur requires the client ID to be sent as a header
    headers = {
        "Authorization": f"Client-ID {token}"
    }

    # Make the request to Imgur API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        images = data["data"]

        # Extract the links to each image
        image_links = [image["link"] for image in images]
        desc = [image["description"] if image["description"] else "No description" for image in images]
        return desc
    else:
        print(f"Failed to fetch album. Status code: {response.status_code}")
        return []

# Fetch images from the album
def get_imgur_album_name(album_id):
    url = f"https://api.imgur.com/3/album/{album_id}"
    headers = {"Authorization": f"Client-ID {token}"}

    # Make the request to Imgur API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        album_title = data['data']['title']
        return album_title
    else:
        return f"Error: Unable to retrieve album info (Status code: {response.status_code})"

# Example usage
album_id = "ZXvh34o"  # Replace with the actual album ID
album_name = get_imgur_album_name(ALBUM_ID)

if album_name:
    print(f"Album Name: {album_name}")

x = {}
for i in album_IDs:
    x[i] = get_imgur_album_name(i)

print(get_imgur_album_images(album_id))

print(x)
# Print the image URLs