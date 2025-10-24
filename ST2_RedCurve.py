import cv2
import numpy as np
import pandas as pd

# Read the data from video
video_path = "IMG_2481.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Video open failed")
    exit()

coords = []  # (frame, x, y)
frame_count = 0

# Loop Frame
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red Range
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    # Red Figure
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
      # Choose red figure
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = np.nan, np.nan
    else:
        cx, cy = np.nan, np.nan

    coords.append([frame_count, cx, cy])

    # Trace
    display = frame.copy()
    if not np.isnan(cx):
        cv2.circle(display, (cx, cy), 10, (0, 255, 255), 2)  # 黄色圆圈标出红球中心
    cv2.putText(display, f"Frame: {frame_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Tracking Red Ball", display)

    # 按 Q 退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# CSV
cap.release()
cv2.destroyAllWindows()

df = pd.DataFrame(coords, columns=["Frame", "X", "Y"])
df.to_csv("mass_point_red_coords.csv", index=False, float_format="%.2f")

print("✅ 文件已保存: mass_point_red_coords.csv")
