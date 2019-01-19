# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import sys
import os

from PIL import Image

from resizeimage import resizeimage


def average_size(image_folder_path, config_file_path):
    file = open(config_file_path, "r")
    sum_height = 0
    sum_width = 0
    nr = 0
    for line in file:
        line1 = line.split(" ")
        image = line1[0]
        image_path = image_folder_path + "/" + image
        image_obj = Image.open(image_path)
        width, height = image_obj.size
        sum_height += height
        sum_width += width
        nr += 1
        
    return sum_width/nr, sum_height/nr

 
def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    print(image_path)
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    #cropped_image.show()


def crop_all(config_file_path, image_folder_path, output_folder, output_config_file):
    file = open(config_file_path, "r") 
    output_file = open(output_config_file, "w")
    for line1 in file: 
        line = line1.split(" ")
        image = line[0]
        logo_name = line[1]
        c1 = int(line[3])
        c2 = int(line[4])
        c3 = int(line[5])
        c4 = int(line[6])
        image_path = os.path.join(image_folder_path, image) # image_folder_path+ '/' + image
        new_name = "c_" + image
        crop(image_path, (c1, c2, c3, c4), output_folder + "/" + new_name)
        output_file.write(new_name + " " + logo_name + "\n")
        
    print("crop done")
        
    file.close()
    output_file.close()


def resize_all(config_file_path, image_folder_path):
    width, height = average_size(image_folder_path, config_file_path)
    file = open(config_file_path, "r") 
    for line in file:
        line1 = line.split(" ")
        image = line1[0]
        print(image + "\n")
        image = os.path.join(image_folder_path, image)
        img = Image.open(image)
        img = resizeimage.resize_thumbnail(img, [int(width), int(height)])
        img.save(image, img.format)
        
    file.close()
        
 
if __name__ == '__main__':
    if sys.argv[1] == "crop":
        config_file_path = sys.argv[2]
        image_folder_path = sys.argv[3]
        output_folder = sys.argv[4]
        output_config_file = sys.argv[5]
        crop_all(config_file_path, image_folder_path, output_folder, output_config_file)
    elif sys.argv[1] == "resize":
        output_config_file = sys.argv[2]
        output_folder = sys.argv[3]
        resize_all(output_config_file, output_folder)
    else:
        config_file_path = sys.argv[1]
        image_folder_path = sys.argv[2]
        output_folder = sys.argv[3]
        output_config_file = sys.argv[4]
        crop_all(config_file_path, image_folder_path, output_folder, output_config_file)
        resize_all(output_config_file, output_folder)

