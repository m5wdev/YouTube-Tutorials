import cv2
from vidgear.gears import CamGear


video_url = 'https://youtu.be/TfOOzM6mPT4'
# video_url = 'https://youtu.be/MDiY0SeyfGw'

# model_path = 'models/haarcascade/haarcascade_fullbody.xml'
model_path = 'models/haarcascade/haarcascade_car.xml'

load_model = cv2.CascadeClassifier(model_path)

options = {
    "STREAM_RESOLUTION": "720p",
    "CAP_PROP_FPS": 30, # framerate 30fps
}
stream = CamGear(source=video_url, stream_mode=True, logging=True, **options).start()


while True:
    frame = stream.read()

    if frame is None:
        break

    frame_to_gray_color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_objects = load_model.detectMultiScale(frame_to_gray_color,
                                                    scaleFactor=1.8,
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


stream.stop()
cv2.destroyAllWindows()
