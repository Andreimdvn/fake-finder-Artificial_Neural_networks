"""
Running this script:
    - param: IMAGE_PATH
    - Uses surf to determine image features and plots them on the image
Import and use this module:
    - use function surf_extract_features
"""

import numpy
import os
import sys
import cv2
import matplotlib.pyplot as plt


def surf_extract_features(image, features=128, threshold=400, plot_image=False):
    """
    Uses surf to search for features in the image
    :param image: image file path
    :param features: number of features to search for
    :param threshold: Hessian threshold
    :param plot_image: True = plot image with features, False = Do not plot
    :return: numpy.ndarray with 1 dimension with the features flattened len = 64*features
    """
    print("Surfing image {} for {} features".format(image, features))
    img = cv2.imread(image, 0)
    # surf = cv2.xfeatures2d.SIFT_create(400)
    surf = cv2.xfeatures2d.SURF_create(threshold)
    kps = surf.detect(img)
    print("Features found: {}. Needed: {}".format(len(kps), features))
    #  best key points based on response
    kps = sorted(kps, key=lambda x: x.response, reverse=True)[:features]

    kps, dsc = surf.compute(img, kps)
    dsc = dsc.flatten()  # make it a 1d array
    if len(kps) < features:
        print("Adding 0 padding for {}/{} necessary features".format(features - len(kps), len(kps)))
        dsc = numpy.concatenate([dsc, numpy.zeros(features - len(kps))])

    if plot_image:
        img2 = cv2.drawKeypoints(img, kps, None, (255, 0, 0), 4)
        plt.imshow(img2), plt.show()

    print("Returning descriptor vector: len:{}(features: {}), data: {}".format(len(dsc), len(kps), dsc))

    return dsc


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: py surf_image IMAGE_PATH")
        sys.exit(1)

    arg = sys.argv[1]
    if not os.path.exists(arg):
        print("ERROR: Path {}does not exist".format(arg))
        sys.exit(2)

    surf_extract_features(arg, plot_image=True)
