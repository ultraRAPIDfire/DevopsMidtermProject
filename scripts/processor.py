import cv2
import os
import numpy as np

# Try importing mediapipe safely
try:
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose_tracker = mp_pose.Pose(static_image_mode=True)
    MEDIAPIPE_AVAILABLE = True
except Exception:
    MEDIAPIPE_AVAILABLE = False


def process_images():
    input_dir = 'inputs'
    output_dir = 'outputs'

    os.makedirs(output_dir, exist_ok=True)

    # If no input images exist, create a dummy one (for CI)
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    if len(os.listdir(input_dir)) == 0:
        dummy = np.zeros((300, 300, 3), dtype=np.uint8)
        cv2.putText(dummy, "TEST", (80, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.imwrite(os.path.join(input_dir, "test.jpg"), dummy)

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        path = os.path.join(input_dir, filename)
        img = cv2.imread(path)
        if img is None:
            continue

        # 1️⃣ Image Reducer
        cv2.imwrite(
            os.path.join(output_dir, f"reduced_{filename}"),
            img,
            [cv2.IMWRITE_JPEG_QUALITY, 10]
        )

        # 2️⃣ Watermark
        watermarked = img.copy()
        cv2.putText(
            watermarked,
            "DEVOPS-MIDTERM",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )
        cv2.imwrite(os.path.join(output_dir, f"watermark_{filename}"), watermarked)

        # 3️⃣ Fisheye Effect
        rows, cols = img.shape[:2]
        map_x, map_y = np.indices((rows, cols), dtype=np.float32)
        map_x = 2 * map_x / (rows - 1) - 1
        map_y = 2 * map_y / (cols - 1) - 1
        r = np.sqrt(map_x ** 2 + map_y ** 2)
        theta = np.arctan2(map_y, map_x)
        r_new = r ** 1.5

        fisheye = cv2.remap(
            img,
            ((r_new * np.cos(theta) + 1) * cols / 2).astype(np.float32),
            ((r_new * np.sin(theta) + 1) * rows / 2).astype(np.float32),
            cv2.INTER_LINEAR
        )

        cv2.imwrite(os.path.join(output_dir, f"fisheye_{filename}"), fisheye)

        # 4️⃣ Pose Detection (Optional)
        pose_img = img.copy()
        if MEDIAPIPE_AVAILABLE:
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = pose_tracker.process(rgb)
            if result.pose_landmarks:
                mp_drawing.draw_landmarks(
                    pose_img,
                    result.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

        cv2.imwrite(os.path.join(output_dir, f"pose_{filename}"), pose_img)

        # 5️⃣ Handwriting / Edge Detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        cv2.imwrite(os.path.join(output_dir, f"handwriting_{filename}"), edges)


if __name__ == "__main__":
    process_images()
