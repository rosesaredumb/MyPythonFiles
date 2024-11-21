import cv2
import numpy as np
import os

imgs_folder = './imgs'
output_name = 'panorama.jpg'

def load_images(image_paths):
    """Load images from paths."""
    images = [cv2.imread(path) for path in image_paths if cv2.imread(path) is not None]
    if len(images) < 2:
        raise ValueError("Need at least two images to stitch.")
    return images

def detect_and_match_features(image1, image2):
    """Detect and match features between two images."""
    detector = cv2.AKAZE_create()  # Feature detector
    keypoints1, descriptors1 = detector.detectAndCompute(image1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(image2, None)

    # Use BRUTEFORCE_HAMMING for binary descriptors
    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
    matches = matcher.knnMatch(descriptors1, descriptors2, k=2)

    # Apply Lowe's ratio test to filter good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    return keypoints1, keypoints2, good_matches

def stitch_pair(image1, image2):
    """Stitch two images based on feature matching and homography."""
    keypoints1, keypoints2, good_matches = detect_and_match_features(image1, image2)

    if len(good_matches) < 10:
        print("Not enough matches found between images!")
        return None

    # Extract matched keypoints
    points1 = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    points2 = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Calculate homography
    H, mask = cv2.findHomography(points2, points1, cv2.RANSAC)

    # Warp the second image to align with the first
    height1, width1 = image1.shape[:2]
    height2, width2 = image2.shape[:2]
    warped_image2 = cv2.warpPerspective(image2, H, (width1 + width2, max(height1, height2)))

    # Combine the images
    stitched_image = np.zeros_like(warped_image2)
    stitched_image[0:height1, 0:width1] = image1
    stitched_image = cv2.addWeighted(stitched_image, 0.5, warped_image2, 0.5, 0)

    return stitched_image

def crop_black_borders(image):
    """Crop black borders from stitched image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        cropped_image = image[y:y + h, x:x + w]
        return cropped_image
    return image

def stitch_images(image_paths):
    """Stitch multiple images in any alignment."""
    images = load_images(image_paths)

    # Start with the first image
    stitched_image = images[0]

    for i in range(1, len(images)):
        print(f"Stitching image {i + 1}...")
        stitched_image = stitch_pair(stitched_image, images[i])
        if stitched_image is None:
            print("Stitching failed!")
            return None

    # Crop black borders
    stitched_image = crop_black_borders(stitched_image)
    return stitched_image

def main():
    # Folder containing images
    image_folder = imgs_folder
    image_paths = [os.path.join(image_folder, f) for f in sorted(os.listdir(image_folder)) if f.endswith(('.jpg', '.png', '.jpeg'))]

    if len(image_paths) < 2:
        print("Need at least two images to stitch!")
        return

    # Perform stitching
    stitched_image = stitch_images(image_paths)
    if stitched_image is not None:
        cv2.imwrite(output_name, stitched_image)
        print(f"Panorama saved as {output_name}")
    else:
        print("Failed to create panorama.")

if __name__ == "__main__":
    main()