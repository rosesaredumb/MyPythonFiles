import cv2
import numpy as np
import os

def stitch_images(image_paths):
    # Load images from given paths
    images = [cv2.imread(image_path) for image_path in image_paths]

    # Initialize the stitcher object
    stitcher = cv2.Stitcher.create() # Corrected line
    # Perform image stitching
    status, stitched_image = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        print("Panorama created successfully!")
        return stitched_image
    else:
        print("Error during stitching")
        return None

def save_panorama(stitched_image, output_path):
    if stitched_image is not None:
        cv2.imwrite(output_path, stitched_image)
        print(f"Panorama saved at {output_path}")
    else:
        print("No image to save.")

def main():
    # List of image paths to stitch
    image_folder = 'imgs'  # Replace with your folder path
    image_paths = [os.path.join(image_folder, f) for f in sorted(os.listdir(image_folder))]

    if len(image_paths) < 2:
        print("Need at least two images to stitch!")
        return

    # Stitch images
    stitched_image = stitch_images(image_paths)

    # Save the stitched panorama
    output_path = 'panorama.jpg'  # Replace with desired output path
    save_panorama(stitched_image, output_path)

if __name__ == "__main__":
    main()