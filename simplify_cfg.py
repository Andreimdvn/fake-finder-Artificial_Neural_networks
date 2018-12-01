import sys
import os


def main(cfg_file):
    img_dict = {}
    with open(cfg_file) as fin:
        for line in fin:
            image_name, logo_class, _, _, _, _, _ = line.strip().split()
            if image_name not in img_dict:
                img_dict[image_name] = logo_class

    with open(cfg_file+".sample", "w") as fout:
        for key in img_dict.keys():
            fout.write("{} {}\n".format(key, img_dict[key]))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: py surf_image IMAGE_PATH")
        sys.exit(1)

    arg = sys.argv[1]
    if not os.path.exists(arg):
        print("ERROR: Path {}does not exist".format(arg))
        sys.exit(2)

    sys.exit(main(sys.argv[1]))
