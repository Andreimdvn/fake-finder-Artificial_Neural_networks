import sys
import os
import rotate_image


def main(cfg_file):
    new_cfg_file = "{}_more{}".format(*os.path.splitext(cfg_file))

    with open (new_cfg_file, "w") as new_cfg_file_handler:
        with open(cfg_file) as fin:
            for line in fin:
                new_cfg_file_handler.write(line)
                my_line = line.strip().split()
                if len(my_line) == 2:
                    image_name, logo_class = my_line
                else:
                    image_name, logo_class, _, _, _, _, _ = my_line
                new_images = rotate_image.rotate_image(os.path.join(os.path.dirname(cfg_file), image_name))
                base_images_paths = [os.path.basename(img) for img in new_images]
                for img in base_images_paths:
                    new_cfg_file_handler.write("{} {}\n".format(img, logo_class))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Takes a config and for each image will create 3 more (rotated at 90, 180, 270) in the same folder")
        print("Usage: py create_more_images.py config_path")
        sys.exit(1)

    arg = sys.argv[1]
    if not os.path.exists(arg):
        print("ERROR: Path {}does not exist".format(arg))
        sys.exit(2)

    sys.exit(main(sys.argv[1]))
