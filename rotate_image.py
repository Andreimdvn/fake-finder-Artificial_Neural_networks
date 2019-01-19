"""
Running this script:
Will rotate a given image 90, -180, 270 degrees and create 3 new images
"""

import os
import sys
import cv2
import imutils


def rotate_img_degree(img, degree, output_name):
    rotated = imutils.rotate_bound(img, degree)
    cv2.imwrite(output_name, rotated)


def flip_image(img, new_flip_path):
    flipped = cv2.flip(img, 0)
    cv2.imwrite(new_flip_path, flipped)


def rotate_image(image_path):
    img = cv2.imread(image_path)
    new_90_path = "{}_90{}".format(*os.path.splitext(image_path))
    new_180_path = "{}_180{}".format(*os.path.splitext(image_path))
    new_270_path = "{}_270{}".format(*os.path.splitext(image_path))
    rotate_img_degree(img, 90, new_90_path)
    rotate_img_degree(img, 180, new_180_path)
    rotate_img_degree(img, 270, new_270_path)
    # new_flip_path = "{}_flip{}".format(*os.path.splitext(image_path))
    # flip_image(img, new_flip_path)

    return new_90_path, new_180_path, new_270_path


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: py rotate_image.py IMAGE_PATH")
        sys.exit(1)

    arg = sys.argv[1]
    if not os.path.exists(arg):
        print("ERROR: Path {}does not exist".format(arg))
        sys.exit(2)

    rotate_image(arg)
