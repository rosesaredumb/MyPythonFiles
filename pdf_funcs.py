import cv2
import numpy as np
import os


imgs_folder = './imgs'
output_name = 'pan.jpg'

def preprocess_images(image_paths):
    """Preprocess images to improve blending and alignment."""
    processed_images = []
    for path in image_paths:
        image = cv2.imread(path)
        if image is None:
            print(f"Error loading image: {path}")
            continue

        # Resize if the image is too large
        height, width = image.shape[:2]
        if height > 1080 or width > 1920:
            scale = 1080 / height
            image = cv2.resize(image, (int(width * scale), 1080))

        # Equalize histogram for better exposure matching
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(image)
        l = cv2.equalizeHist(l)
        image = cv2.merge((l, a, b))
        image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)

        processed_images.append(image)
    return processed_images

def stitch_images(image_paths):
    """Stitch images together with enhanced blending."""
    images = preprocess_images(image_paths)

    if len(images) < 2:
        print("Need at least two valid images to stitch!")
        return None

    # Initialize OpenCV Stitcher
    stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)  # Use Panorama mode

    # Set confidence threshold for better blending
    stitcher.setPanoConfidenceThresh(0.8)  # Adjust threshold as needed

    # Perform stitching
    print("Stitching images...")
    status, stitched_image = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        print("Panorama created successfully!")
        return stitched_image
    else:
        print(f"Stitching failed with error code: {status}")
        return None

def crop_black_borders(image):
    """Crop black borders from the stitched panorama."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours to determine the bounding box
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        cropped_image = image[y:y + h, x:x + w]
        print("Cropped black borders.")
        return cropped_image
    return image

def save_panorama(stitched_image, output_path):
    """Save the stitched panorama to disk."""
    if stitched_image is not None:
        cv2.imwrite(output_path, stitched_image)
        print(f"Panorama saved at {output_path}")
    else:
        print("No image to save.")

def main():
    # Folder containing images to stitch
    image_folder = imgs_folder  # Replace with your folder path
    image_paths = [os.path.join(image_folder, f) for f in sorted(os.listdir(image_folder)) if f.endswith(('.jpg', '.png', '.jpeg'))]

    if len(image_paths) < 2:
        print("Need at least two images to stitch!")
        return

    # Stitch images
    stitched_image = stitch_images(image_paths)
    if stitched_image is not None:
        # Crop black borders if needed
        stitched_image = crop_black_borders(stitched_image)

        # Save the final panorama
        output_path = output_name  # Replace with desired output path
        save_panorama(stitched_image, output_path)

if __name__ == "__main__":
    main()