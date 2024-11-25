import cv2
import os

def load_images_from_folder(folder_path):
    """
    Load all images from a given folder.
    """
    images = []
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
    return images

def stitch_images(images):
    """
    Stitch the list of images into a single panorama.
    """
    # Create a Stitcher object (for OpenCV 4.x)
    stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)
    # Perform the stitching process
    status, stitched_image = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        print("Images stitched successfully!")
        return stitched_image
    else:
        print(f"Image stitching failed with status code: {status}")
        return None

def save_image(output_path, image):
    """
    Save the stitched image to a file.
    """
    cv2.imwrite(output_path, image)
    print(f"Stitched image saved to: {output_path}")

if __name__ == "__main__":
    # Path to the folder containing input images
    input_folder = "imgs"  # Change this to your folder path
    output_file = "stitched_globe_panorama.jpg"

    # Load images from the folder
    images = load_images_from_folder(input_folder)

    if len(images) < 2:
        print("Need at least two images for stitching.")
    else:
        # Stitch the images
        panorama = stitch_images(images)

        if panorama is not None:
            # Save the output panorama image
            save_image(output_file, panorama)
            # Show the result
            cv2.imshow("Stitched Panorama", panorama)
            cv2.waitKey(0)
            cv2.destroyAllWindows()