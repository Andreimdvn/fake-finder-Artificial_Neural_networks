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

f = open("features.txt",'w')


def surf_extract_features(image, features=512, threshold=400, plot_image=False):
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
    features_found = len(kps)
    f.write("{}\n".format(len(kps)))
    #  best key points based on response
    kps = sorted(kps, key=lambda x: x.response, reverse=True)[:features]

    kps, dsc = surf.compute(img, kps)
    out_file = open("wtf_output.txt", 'w')
    if dsc is None:
        print("\n\n\nwtf {}\n\n\n".format(image))
        out_file.write("!!! ERROR AT IMAGE SURF {}\n".format(image))
        return [0] * (features * 64), 0
    dsc = dsc.flatten()  # make it a 1d array
    if len(kps) < features:
        print("Adding 0 padding for {}/{} necessary features".format(features - len(kps), len(kps)))
        dsc = numpy.concatenate([dsc, numpy.zeros((features - len(kps))*64)])

    if plot_image:
        img2 = cv2.drawKeypoints(img, kps, None, (255, 0, 0), 4)
        plt.imshow(img2), plt.show()

    # print("Returning descriptor vector: shape:{}(features: {}), data: {}".format(dsc.shape, len(kps), dsc))

    return dsc, features_found


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: py surf_image IMAGE_PATH")
        sys.exit(1)

    arg = sys.argv[1]
    if not os.path.exists(arg):
        print("ERROR: Path {}does not exist".format(arg))
        sys.exit(2)

    surf_extract_features(arg, plot_image=True)
