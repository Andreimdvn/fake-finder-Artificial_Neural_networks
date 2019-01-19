import sys
import os
from random import shuffle


def main(cfg_file):
    images_for_class = {}
    with open(cfg_file) as fin:
        for line in fin:
            my_line = line.strip().split()
            if len(my_line) == 2:
                image_name, logo_class = my_line
            else:
                image_name, logo_class, _, _, _, _, _ = my_line
            if logo_class not in images_for_class:
                images_for_class[logo_class] = []
            if image_name not in images_for_class[logo_class]:
                images_for_class[logo_class].append(image_name)

    train_tuples = []
    test_tuples = []

    for logo_class in images_for_class.keys():
        images = images_for_class[logo_class]
        # print(images[:int(0.7*len(images))])
        shuffle(images)
        train_tuples += [(image, logo_class) for image in images[:int(0.7*len(images))]]
        test_tuples += [(image, logo_class) for image in images[int(0.7*len(images)):]]

    shuffle(train_tuples)

    print(test_tuples)

    out_file_base = os.path.splitext(cfg_file)[0]
    with open(out_file_base+".train", "w") as fout:
        for image, logo in train_tuples:
            fout.write("{} {}\n".format(image, logo))

    with open(out_file_base+".test", "w") as fout:
        for image, logo in test_tuples:
            fout.write("{} {}\n".format(image, logo))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Takes a config and reduces it to single logo per image => train + test 70 - 30 taking into account equal"
              " logo distribution")
        print("Usage: py simplify_cfg cfg_path")
        sys.exit(1)

    arg = sys.argv[1]
    if not os.path.exists(arg):
        print("ERROR: Path {}does not exist".format(arg))
        sys.exit(2)

    sys.exit(main(sys.argv[1]))
