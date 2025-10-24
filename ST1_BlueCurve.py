import cv2
import numpy as np
import pandas as pd

# Read the data from the video
video_path = "IMG_2481.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Video open failed")
    exit()

coords = []  #(frame, x, y)
frame_count = 0

# Frame Loop Process
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Blue Color
    # HSV_Range H: [100,140], S: [100,255], V: [50,255]
    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([140, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    # Look up for Figure
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Max Figure
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

    # Show up
    display = frame.copy()
    if not np.isnan(cx):
        cv2.circle(display, (cx, cy), 10, (0, 255, 255), 2)  # 黄色圆点
    cv2.putText(display, f"Frame: {frame_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Tracking", display)

    # Quit with Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# CSV File
df = pd.DataFrame(coords, columns=["Frame", "X", "Y"])
df.to_csv("mass_point_blue_coords.csv", index=False, float_format="%.2f")

print(" File -> mass_point_blue_coords.csv ")

