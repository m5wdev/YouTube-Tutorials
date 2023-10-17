import cv2


video_file_path = 'video/video1.mp4'
model_path = 'models/haarcascade/haarcascade_fullbody.xml'
load_model = cv2.CascadeClassifier(model_path)

video = cv2.VideoCapture(video_file_path)

while True:
    # avoid error: (-215:Assertion failed) !_src.empty()
    if video.isOpened():
        ret, frame = video.read() # .read() Grabs, decodes and returns the next video frame

        if ret is not True:
            break

    frame_to_gray_color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_objects = load_model.detectMultiScale(frame_to_gray_color,
                                                    scaleFactor=1.9,
                                                    minNeighbors=1
                                                )

    # Draw rectangles ob detected objects
    for x, y, width, height in detected_objects:
        cv2.rectangle(frame,
                        pt1=(x, y), pt2=(x + width, y + height),
                        color=(0, 255, 0), thickness=2
                    )

    cv2.imshow('Detected objects', frame)

    # press Esc to exit
    # if cv2.waitKey(1) == 27: # faster
    #     break
    if cv2.waitKey(33) == 27: # slower
        break


video.release()
cv2.destroyAllWindows()
