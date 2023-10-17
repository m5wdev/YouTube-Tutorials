import cv2
import numpy as np


# image = cv2.imread('images/image1.jpg')
image = cv2.imread('images/image2.jpg')

model_prototxt_path = 'models/caffemodel/MobileNetSSD_deploy.prototxt'
model_caffemodel_path = 'models/caffemodel/MobileNetSSD_deploy.caffemodel'
load_model = cv2.dnn.readNetFromCaffe(model_prototxt_path, model_caffemodel_path)

minimal_confidence = 0.1

categories_list = ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

# generate color for each category
np.random.seed(600000) # for better colors
colors = np.random.uniform(0, 255, size=(len(categories_list), 3))


height, width = image.shape[0], image.shape[1]
# blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007, (300, 300), 130) # blob (Binary Large Object)
blob = cv2.dnn.blobFromImage(cv2.resize(image, (2000, 2000)), 0.007, (2000, 2000), 130) # blob (Binary Large Object)

load_model.setInput(blob)
detected_objects = load_model.forward()
# print(detected_objects)

for i in range(detected_objects.shape[2]):
    confidence = detected_objects[0][0][i][2]

    if confidence > minimal_confidence:
        category_index = int(detected_objects[0, 0, i, 1])

        upper_left_x = int(detected_objects[0, 0, i, 3] * width)
        upper_left_y = int(detected_objects[0, 0, i, 4] * height)
        lower_right_x = int(detected_objects[0, 0, i, 5] * width)
        lower_right_y = int(detected_objects[0, 0, i, 6] * height)

        # draw rectangle
        cv2.rectangle(image, (upper_left_x, upper_left_y), (lower_right_x, lower_right_y), colors[category_index], 2)

        # put text in upper part of rectangle
        format_confidence = '100' if round(confidence, 1) == 1.0 else f'{confidence:.2f}'.replace('0.', '')
        detected_obj_text = f'{categories_list[category_index]}: {format_confidence}%'
        cv2.putText(image, detected_obj_text,
                    (upper_left_x, upper_left_y - 15 if upper_left_y > 30 else upper_left_y + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors[category_index], 2)

cv2.imshow('Detected Objects', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
