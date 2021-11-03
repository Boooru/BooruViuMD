import os
from PIL import Image


def folder_to_png(path: str, output_folder: str = "./pngs", cleanup: bool = False):
    if os.path.isdir(path):
        original_files = os.listdir(path)
        for image in original_files:
            image_name = image.split(".")[0]
            im = Image.open(path + "/" + image)
            im.save(output_folder + "/" + image_name + ".png")

        if cleanup:
            for file in original_files:
                os.remove(path + "/" + file)


if __name__ == '__main__':
    print("What folder?")
    inp = input()
    print("What output?")
    output = input()

    print("Converting to png...")
    folder_to_png(inp, output)
    print("Done!")
