import cv2
import pandas as pd
from datetime import datetime

first_img = None
status_list = [0]
times_list = []
data_frame = pd.DataFrame(columns=["Start", "End"])
# Param - How many cams
video = cv2.VideoCapture(0)

while True:
    # Capturing video
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    if first_img is None:
        first_img = gray
        continue

    delta_frame = cv2.absdiff(first_img, gray)
    w_b_delta = cv2.threshold(delta_frame, 40, 255, cv2.THRESH_BINARY)[1]
    # Remove smooth from img
    w_b_delta = cv2.dilate(w_b_delta, None, iterations=2)

    # Find contour / draw contour
    (_,cnts,_) = cv2.findContours(w_b_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for countour in cnts:
        if cv2.contourArea(countour) < 7000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(countour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)

    status_list.append(status)
    # Save time of detection
    if status_list[-1] == 1 and status_list[-2] == 0:
        times_list.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times_list.append(datetime.now())

    cv2.imshow("Capturing_web_cam", gray)
    cv2.imshow("Diff", delta_frame)
    cv2.imshow("New_Diff", w_b_delta)
    cv2.imshow("Color Frame new", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if len(times_list)%2 != 0:
            times_list.append(datetime.now())
        break

# save time in CSV
for i in range(0, len(times_list), 2):
    data_frame = data_frame.append({"Start": times_list[i], "End": times_list[i+1]}, ignore_index=True)

data_frame.to_csv("Detection_time.csv")
video.release()
cv2.destroyAllWindows()