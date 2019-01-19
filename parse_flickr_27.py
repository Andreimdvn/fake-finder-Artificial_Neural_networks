"""
Will extract(filter) images with  a given logo class
from an existing folder to a new folder another one using config of first folder.
Also creates a new config for output folder
"""
import traceback
import argparse
import sys
import os
import shutil


DEFAULT_CONFIG = "flickr_logos_27_dataset_training_set_annotation.txt"
DEFAULT_SOURCE = "source_folder"
DEFAULT_DESTINATION = "output_folder"


def read_classes(file_logo_class):
    classes = set()
    with open(file_logo_class) as fin:
        for line in fin:
            line = line.strip()
            if line not in classes:
                classes.add(line)

    print("Classes: {}".format(classes))
    return classes


def extract_images(config, source, destination, file_logo_class):
    if not os.path.exists(destination):
        os.mkdir(destination)

    if not os.path.exists(file_logo_class):
        print("Logo file class {} does not exists!".format(file_logo_class))
        return

    classes = read_classes(file_logo_class)

    output_path = os.path.join(destination, 'data.txt')
    print("Will extract(filter) images with logo class in {} from {} to folder using config {} + creating new config {}"
          .format(classes, source, destination, config, output_path))

    count = 0
    config_entries = 0
    with open(output_path, "w") as fout:
        with open(config) as fin:
            for line in fin:
                for logo_class in classes:
                    if logo_class in line:
                        try:
                            file_name = line.strip().split()[0]
                            src = os.path.join(source, file_name)
                            dst = os.path.join(destination, file_name)
                            if not os.path.exists(dst):
                                print("Copying {} to {}".format(src, dst))
                                fout.write(line)
                                shutil.copy2(src, dst)
                                count += 1
                            config_entries += 1
                            fout.write(line)
                        except Exception as ex:
                            print("ERROR: Ex: {}, Traceback: {}".format(ex, traceback.format_exc()))

    print("Total config_entries: {}. Total files {} files".format(config_entries, count))


def main():
    parser = argparse.ArgumentParser(
        description="Extracts images by class from images_folder described in config_file. "
                    "Extract destination: 'destination'")
    parser.add_argument("-c", "--config", type=str, help="path to file that describes the images", default=DEFAULT_CONFIG)
    parser.add_argument("-s", "--source", type=str, help="images source folder", default=DEFAULT_SOURCE)
    parser.add_argument("-d", "--destination", type=str, help="folder destination", default=DEFAULT_DESTINATION)
    parser.add_argument("-k", "--file_with_logo_classes", type=str, help="file with classes of images to extract, "
                                                                         "one per line", required=True)

    args = parser.parse_args()
    print("Got args: {}".format(args))

    return extract_images(args.config, args.source, args.destination, args.file_with_logo_classes)


if __name__ == '__main__':
    sys.exit(main())
