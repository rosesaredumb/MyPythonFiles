import requests

from discord_bot.v2024.settings import retrieve_keys

# Replace this with your actual Imgur Client ID

ALBUM_ID = "d9OwJIB"  # The album ID you want to fetch
token = str(retrieve_keys("imgur_client_ID"))

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
        return image_links
    else:
        print(f"Failed to fetch album. Status code: {response.status_code}")
        return []

# Fetch images from the album
album_images = get_imgur_album_images(ALBUM_ID)

# Print the image URLs
for img_url in album_images:
    print(img_url)