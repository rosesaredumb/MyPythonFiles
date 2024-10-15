import requests

# Replace 'your-client-id' with the Client ID from your Imgur application
CLIENT_ID = '2ea349879154d4a'
USERNAME = 'twentythreelives'  # Replace with the Imgur username

# Base URL for Imgur API
url = f'https://api.imgur.com/3/account/{USERNAME}/albums'

# Headers with your Client ID
headers = {
    'Authorization': f'Client-ID {CLIENT_ID}'
}

# Send a GET request to the Imgur API to fetch albums
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print(data)
    # Extract the list of albums
    albums = data["data"]
    print(albums)
    print("ni")
    # Loop through each album and print its ID and title
    for album in albums:
        print("ni")
        print(f"Album ID: {album['id']}, Title: {album['title']}")
else:
    print(f"Failed to retrieve albums. Status code: {response.status_code}")