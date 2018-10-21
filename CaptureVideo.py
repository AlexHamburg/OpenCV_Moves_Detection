import cv2, time
# How many cams
video = cv2.VideoCapture(0)
nb_of_frames = 0
while True:
    # Capturing video
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #time.sleep(3)
    nb_of_frames += 1
    print(check)
    print(frame)
    cv2.imshow("Capturing_web_cam", gray)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
print(nb_of_frames)
video.release()
cv2.destroyAllWindows()
