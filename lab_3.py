import sys
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from scipy import signal

def image_to_np_array(image_path):
    return np.asarray(Image.open(image_path).convert("L"))

def normalized_image(image_array):
    floor_value = image_array.min()
    ceiling_value = image_array.max()
    scale = (ceiling_value - floor_value) / 255

    return (image_array - floor_value) / scale

def corner_detection(image_aw, image_bw, image_cw):
    rows, cols = image_aw.shape
    eigen_threshold = 90000
    result_image = Image.open("input_image.png").convert("RGB")
    draw_result = ImageDraw.Draw(result_image)
    for i in range(rows):
        for j in range(cols):
            matrix = np.array([[image_aw[i][j], image_bw[i][j]], 
                    [image_bw[i][j], image_cw[i][j]]])
            eigenvalues, eigenvectors = np.linalg.eig(matrix)
            min_eigenvalue = min(eigenvalues)
            if min_eigenvalue > eigen_threshold:
                draw_result.line(((j-7, i), (j+7, i)), fill = (255, 0, 0))
                draw_result.line(((j, i-7), (j, i+7)), fill = (255, 0, 0))
    
    result_image.save("corner_detected_image.png")


if __name__ == "__main__":

    args = sys.argv
    if len(args) != 2:
        print("Please enter only the image file path as a command line argument.")
        sys.exit()

    image_array = image_to_np_array(args[1])

    horizontal_derivative = np.zeros((3,3))
    horizontal_derivative[1][0] = -1
    horizontal_derivative[1][2] = 1

    vertical_derivative = np.zeros((3,3))
    vertical_derivative[0][1] = -1
    vertical_derivative[2][1] = 1

    image_ix = signal.convolve2d(image_array, horizontal_derivative)
    image_iy = signal.convolve2d(image_array, vertical_derivative)

    image_ix_2 = image_ix * image_ix
    image_ix_iy = image_ix * image_iy
    image_iy_2 = image_iy * image_iy
    box_filter = np.ones((3,3))

    image_aw = signal.convolve2d(image_ix_2, box_filter)
    image_bw = signal.convolve2d(image_ix_iy, box_filter)
    image_cw = signal.convolve2d(image_iy_2, box_filter)

    corner_detection(image_aw, image_bw, image_cw)
