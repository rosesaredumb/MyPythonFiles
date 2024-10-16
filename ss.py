import requests


class imgur_functions:
    def __init__(self):
        pass

    def get_imgur_album_images_with_descriptions(self, album_id: str):
        # Imgur API endpoint to get album images
        url = f"https://api.imgur.com/3/album/{album_id}/images"
        id = '2ea349879154d4a'
        # Imgur requires the client ID to be sent as a header
        headers = {
            "Authorization": f"Client-ID {id}"
        }

        # Make the request to Imgur API
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            images = data["data"]

            # Extract the links and descriptions of each image
            image_data = {"None":[]}
            for image in images:
                if image["description"]:
                    if image["description"] not in image_data:
                        image_data[image["description"]] = [image["link"]]

                    elif image["description"] in image_data:
                        image_data[image["description"]].append(image["link"])

                else:
                    image_data["None"].append(image["link"])
            
            titles = list(image_data.keys())

            return image_data, titles
        else:
            print(f"Failed to fetch album. Status code: {response.status_code}")
            return []
        
    def get_topic_names(self, album_id):
        whole_data = self.get_imgur_album_images_with_descriptions(album_id)[0]

        pp = input("name?")
        url_list = whole_data[pp]
        return url_list


# Usage example:
imgur_instance = imgur_functions()
album_id = "ZXvh34o"  # Replace with your actual album ID

# Get image links and descriptions from the album
images_with_descriptions = imgur_instance.get_imgur_album_images_with_descriptions(album_id)

# Display the results
print(images_with_descriptions)
#print(imgur_instance.get_topic_names(album_id))
