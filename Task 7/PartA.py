import cv2
import numpy as np
from matplotlib import pyplot as plt

input_image = cv2.imread("image2.png")
height = input_image.shape[0]
width = input_image.shape[1]
black_thresh = 80
blue_thresh = 150
x_coords = []
y_coords = []
final = []

for i in range(height):
    avg = np.zeros((3,))
    for j in range(width):
        avg += input_image[i][j] / width
    if np.average(avg) < black_thresh:
        y_coords.append(i)
        for j in range(width):
            input_image[i][j] = [0, 0, 0]

for i in range(width):
    avg = np.zeros((3,))
    for j in range(height):
        avg += input_image[j][i] / height
    if np.average(avg) < black_thresh:
        x_coords.append(i)
        for j in range(height):
            input_image[j][i] = [0, 0, 0]

columns = len(x_coords) - 1
rows = len(y_coords) - 1

for i in range(rows):
    arr = []
    for j in range(columns):
        avg = np.zeros((3,))
        for a in range(y_coords[i] + 1, y_coords[i + 1]):
            for b in range(x_coords[j] + 1, x_coords[j + 1]):
                avg += input_image[a][b] / ((y_coords[i + 1] - y_coords[i] - 1) * (x_coords[j + 1] - x_coords[j] - 1))
        if avg[0] > blue_thresh:
            arr.append(1)
        else:
            arr.append(0)
        for a in range(y_coords[i] + 1, y_coords[i + 1]):
            for b in range(x_coords[j] + 1, x_coords[j + 1]):
                if arr[-1] == 1:
                    input_image[a][b] = [255, 0, 0]
                else:
                    input_image[a][b] = [0, 255, 255]
    final.append(arr)

b, g, r = cv2.split(input_image)
input_image = cv2.merge([r, g, b])

plt.imshow(input_image)
plt.show()