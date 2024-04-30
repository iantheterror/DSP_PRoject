from PIL import Image,ExifTags

import os

def resize_images_in_folder(input_folder, output_folder, height, nf,counter):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg",".JPG")):
            
            newname = f'{nf}_{counter}.jpg'
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, newname)
            

            # Open the image file
            with Image.open(input_path) as img:
                '''for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                    exif = dict(img._getexif().items())

                    if exif[orientation] == 3:
                        img = img.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        img = img.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        img = img.rotate(90, expand=True)'''
    
                original_width, original_height = img.size
                aspect_ratio = original_width / original_height
                original_max = max(original_height,original_width)
                size_ratio = original_max/height

                new_width = int(original_width/size_ratio)
                new_height = int(original_height/size_ratio)
                print(f'file: {filename} Original Size: {original_height}X{original_width}')
                print(f'Size Ratio: {size_ratio} Aspect Ratio: {aspect_ratio}  New Size: {new_height}X{new_width}')
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                # Save the resized image to the output path
                resized_img.save(output_path)
                counter +=1

if __name__ == "__main__":
    # Input parameters
    start_counter = 1
    newfilename = "resized4"
    input_folder = "original_images/"  # Folder containing input images
    output_folder = "resized_images/"  # Output folder for resized images
    new_height = 640  # New height for the resized images
    #resize is determined by size ratio, so if the input is 1280X960  the output will be 640X480

    # Resize images in the input folder and save to the output folder
    resize_images_in_folder(input_folder, output_folder, new_height, newfilename,start_counter)
    print("Batch resizing completed.")
