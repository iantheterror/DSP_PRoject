import os
import shutil

input_folder = "resized_images/"
label = "tagged_images/labels/"
img="tagged_images/images/"
counter = 0
endpath = ""
validate = 5  #1 in X

for filename in os.listdir(input_folder):
    if filename.endswith((".jpg")):
        counter +=1
        if filename == "classes.txt":
            continue
        else:
            print(filename)
            if counter % validate == 0:
                endpath = "val/"
            else:
                endpath = "train/"

            file = os.path.splitext(os.path.basename(filename))[0]

            
            txt_name = file + ".txt"

            img_path = os.path.join(img, endpath, filename)
            txt_path = os.path.join(label, endpath, txt_name)

            os.makedirs(os.path.dirname(txt_path), exist_ok=True)
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
        # Copy .txt file to label directory
            shutil.copy(os.path.join(input_folder, filename), img_path)

        # Copy corresponding .jpg file to images directory
            shutil.copy(os.path.join(input_folder, txt_name), txt_path)


