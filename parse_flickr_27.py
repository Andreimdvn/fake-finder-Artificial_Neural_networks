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


def extract_images(config, source, destination, logo_class):
    if not os.path.exists(destination):
        os.mkdir(destination)

    output_path = os.path.join(destination, logo_class)
    print("Will extract(filter) images with logo class {} from {} to folder using config {} + creating new config {}"
          .format(logo_class, source, destination, config, output_path))

    count = 0
    config_entries = 0
    with open(output_path, "w") as fout:
        with open(config) as fin:
            for line in fin:
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
                        print("ERROR: Ex: {}, Traceback: {}".format(ex, traceback.format_exc))

    print("Total config_entries: {}. Total files {} files".format(config_entries, count))


def main():
    parser = argparse.ArgumentParser(
        description="Extracts images by class from images_folder described in config_file. "
                    "Extract destination: 'destination'")
    parser.add_argument("-c", "--config", type=str, help="path to file that describes the images", default=DEFAULT_CONFIG)
    parser.add_argument("-s", "--source", type=str, help="images source folder", default=DEFAULT_SOURCE)
    parser.add_argument("-d", "--destination", type=str, help="folder destination", default=DEFAULT_DESTINATION)
    parser.add_argument("-k", "--logo_class", type=str, help="class of images to extract", required=True)

    args = parser.parse_args()
    print("Got args: {}".format(args))

    return extract_images(args.config, args.source, args.destination, args.logo_class)


if __name__ == '__main__':
    sys.exit(main())
