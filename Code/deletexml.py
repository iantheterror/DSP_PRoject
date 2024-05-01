import os

directory = 'resized_images/'
N = 1
files = os.listdir(directory)

for filename in files:
    if filename.startswith(f'resized{N}') and filename.endswith('.xml.txt'):
        try:
            n = int(filename.split('_')[1].split('.')[0])
            # Construct the new filename with the .xml extension removed
            new_filename = f"resized{N}_{n}.txt"
            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"Renamed {filename} to {new_filename}")
        except (IndexError, ValueError):
            print(f"Issue with filename format: {filename}")