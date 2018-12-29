import sys
import os
from random import shuffle


def main(cfg_file):
    img_dict = {}
    with open(cfg_file) as fin:
        for line in fin:
            image_name, logo_class, _, _, _, _, _ = line.strip().split()
            if image_name not in img_dict:
                img_dict[image_name] = logo_class

    all_keys = list(img_dict.keys())
    shuffle(all_keys)
    train_keys = all_keys[:int(0.7*len(all_keys))]
    test_keys = all_keys[int(0.7*len(all_keys)):]

    with open(cfg_file+"_train.sample", "w") as fout:
        for key in train_keys:
            fout.write("{} {}\n".format(key, img_dict[key]))

    with open(cfg_file+"_test.sample", "w") as fout:
        for key in test_keys:
            fout.write("{} {}\n".format(key, img_dict[key]))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Takes a config and reduces it to single logo per image => train + test 70 - 30")
        print("Usage: py simplify_cfg cfg_path")
        sys.exit(1)

    arg = sys.argv[1]
    if not os.path.exists(arg):
        print("ERROR: Path {}does not exist".format(arg))
        sys.exit(2)

    sys.exit(main(sys.argv[1]))
