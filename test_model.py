"""
Running this script:
    - param: IMAGE_PATH
    - Uses surf to determine image features and plots them on the image
Import and use this module:
    - use function surf_extract_features
"""

import os
import sys

import keras

from train_model import test_model, get_file_data

f = open("features.txt",'w')


def main(model_path, test_data_path):
    model = keras.models.load_model(model_path)
    x_test_data, y_test_data, classes = get_file_data(test_data_path)
    test_model(model, x_test_data, y_test_data)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: py test_model.py MODEL_CFG_PATH TEST_DATA_PATH")
        sys.exit(1)

    model_path = sys.argv[1]
    test_data_path = sys.argv[2]
    if not os.path.exists(model_path):
        print("ERROR: Path {}does not exist".format(model_path))
        sys.exit(2)

    if not os.path.exists(test_data_path):
        print("ERROR: Path {}does not exist".format(test_data_path))
        sys.exit(2)

    main(model_path, test_data_path)
