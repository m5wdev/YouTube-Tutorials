import cv2


image = 'images/image1.jpg'
# image = 'images/image2.jpg'

model_path = 'models/haarcascade/haarcascade_fullbody.xml'
# model_path = 'models/haarcascade/haarcascade_lowerbody.xml'
# model_path = 'models/haarcascade/haarcascade_car.xml'
load_model = cv2.CascadeClassifier(model_path)

read_image = cv2.imread(image)

detected_objects = load_model.detectMultiScale(read_image,
                                                    scaleFactor=1.1,
                                                    minNeighbors=1
                                                )
# print(detected_objects)

for x, y, width, height in detected_objects:
    cv2.rectangle(read_image,
                    pt1=(x, y), pt2=(x + width, y + height),
                    color=(0, 255, 0), thickness=2
                )

cv2.imshow('image', read_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
