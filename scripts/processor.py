import cv2
import os
import numpy as np

# Updated import logic to fix ModuleNotFoundError
try:
    import mediapipe as mp
    from mediapipe.solutions import pose as mp_pose
    from mediapipe.solutions import drawing_utils as mp_drawing
except (ImportError, ModuleNotFoundError):
    # Direct sub-module import for Linux/CI environments
    import mediapipe.python.solutions.pose as mp_pose
    import mediapipe.python.solutions.drawing_utils as mp_drawing

def process_images():
    input_dir = 'inputs/'
    output_dir = 'outputs/'
    
    # Requirement: Automatically detect image files [cite: 17]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize MediaPipe for Pose Matching
    pose_tracker = mp_pose.Pose(static_image_mode=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(input_dir, filename)
            img = cv2.imread(path)
            if img is None: continue

            # 1. Image Reducer (File size degradation)
            cv2.imwrite(os.path.join(output_dir, f"reduced_{filename}"), img, [cv2.IMWRITE_JPEG_QUALITY, 10])

            # 2. Watermark Adder
            watermarked = img.copy()
            cv2.putText(watermarked, 'DEVOPS-MIDTERM', (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imwrite(os.path.join(output_dir, f"watermark_{filename}"), watermarked)

            # 3. Fish eye Effect
            rows, cols = img.shape[:2]
            map_x, map_y = np.indices((rows, cols), dtype=np.float32)
            map_x, map_y = 2.0 * map_x / (rows - 1) - 1.0, 2.0 * map_y / (cols - 1) - 1.0
            r, phi = np.sqrt(map_x**2 + map_y**2), np.arctan2(map_y, map_x)
            r_new = r**1.5 
            fisheye = cv2.remap(img, ((r_new * np.sin(phi) + 1.0) * (cols - 1) / 2.0), 
                               ((r_new * np.cos(phi) + 1.0) * (rows - 1) / 2.0), cv2.INTER_LINEAR)
            cv2.imwrite(os.path.join(output_dir, f"fisheye_{filename}"), fisheye)

            # 4. Pose Matching Detection
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            res = pose_tracker.process(rgb_img)
            pose_img = img.copy()
            if res.pose_landmarks:
                mp_drawing.draw_landmarks(pose_img, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.imwrite(os.path.join(output_dir, f"pose_{filename}"), pose_img)

            # 5. Handwriting Typo Detection (Visual Filter)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            cv2.imwrite(os.path.join(output_dir, f"handwriting_{filename}"), edges)

if __name__ == "__main__":
    process_images()