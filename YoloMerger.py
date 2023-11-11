import os
import re
import yaml
import shutil
import random
from PIL import Image

#List of supported classes

#Full list of classes
full_classes_color = {'double bottom':[0,0,255], 'double top':[0,255,0], 'descending triangle':[255,0,255],'ascending triangle':[255,255,0],
                 'triple bottom':[255,0,0], 'inverse head and shoulders':[128,0,0], 'triple top':[0,255,255], 'head and shoulders':[0,128,0]
                 ,'symmetrical triangle':[0,0,128]}
full_classes_id = {'double bottom':0, 'double top':1, 'descending triangle':2, 'ascending triangle':3, 'triple bottom':4,
                'inverse head and shoulders':5,'triple top':6, 'head and shoulders':7,'symmetrical triangle':8}

classes_color = {'double bottom':[0,0,255], 'double top':[0,255,0], 'head and shoulders':[0,128,0]}
classes_id = {'double bottom':0, 'double top':1, 'head and shoulders':2}


#Dataset path used to normalized
#Dataset path used as reference
dataset_source_path = "D:/Freelance/stock_patterns/datasets/roboflow/3p_1k5_custom/"
dataset_target_path = "D:/Freelance/stock_patterns/datasets/roboflow/3p_1k5_custom_640/"

def split_train_val_dataset(dataset_source_path, percentage):
    # Paths to train and validation image/label directories
    images_train_path = os.path.join(dataset_source_path, 'images', 'train')
    labels_train_path = os.path.join(dataset_source_path, 'labels', 'train')
    images_val_path = os.path.join(dataset_source_path, 'images', 'val')
    labels_val_path = os.path.join(dataset_source_path, 'labels', 'val')

    # Get list of all image files
    all_images = [f for f in os.listdir(images_train_path) if os.path.isfile(os.path.join(images_train_path, f))]

    # Randomly sample a subset of the image files
    num_to_sample = int(len(all_images) * percentage)
    sampled_images = random.sample(all_images, num_to_sample)

    # Move the sampled image files and their associated labels
    for image_file in sampled_images:
        # Move image
        shutil.move(os.path.join(images_train_path, image_file), os.path.join(images_val_path, image_file))

        # Move corresponding label
        label_file = image_file.rsplit('.', 1)[0] + '.txt'
        shutil.move(os.path.join(labels_train_path, label_file), os.path.join(labels_val_path, label_file))


def resize_images_and_copy_annotations(dataset_source_path, dataset_target_path, new_size=(640, 360)):
    # Create target directories if they don't exist
    for subdir in ['train', 'val']:
        os.makedirs(os.path.join(dataset_target_path, 'images', subdir), exist_ok=True)
        os.makedirs(os.path.join(dataset_target_path, 'labels', subdir), exist_ok=True)

    # Resize images
    for subdir in ['train', 'val']:
        images_source_dir = os.path.join(dataset_source_path, 'images', subdir)
        images_target_dir = os.path.join(dataset_target_path, 'images', subdir)

        for image_name in os.listdir(images_source_dir):
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Open the image
                image_path = os.path.join(images_source_dir, image_name)
                with Image.open(image_path) as img:
                    # Resize the image
                    img_resized = img.resize(new_size, Image.ANTIALIAS)

                    # Save the resized image to the target directory
                    img_resized.save(os.path.join(images_target_dir, image_name))

    # Copy annotations
    for subdir in ['train', 'val']:
        labels_source_dir = os.path.join(dataset_source_path, 'labels', subdir)
        labels_target_dir = os.path.join(dataset_target_path, 'labels', subdir)

        for label_name in os.listdir(labels_source_dir):
            source_label_path = os.path.join(labels_source_dir, label_name)
            target_label_path = os.path.join(labels_target_dir, label_name)

            # Copy the annotation file to the target directory
            shutil.copy2(source_label_path, target_label_path)

def remove_empty_annotations_and_images(dataset_source_path):
    for subdir in ['train', 'val']:
        labels_dir = os.path.join(dataset_source_path, 'labels', subdir)
        images_dir = os.path.join(dataset_source_path, 'images', subdir)

        for filename in os.listdir(labels_dir):
            file_path = os.path.join(labels_dir, filename)
            # Check if the .txt file is empty
            if os.path.getsize(file_path) == 0:
                print(f"Removing empty file: {file_path}")
                os.remove(file_path)  # Remove the empty .txt file

                # Construct the image file path based on the .txt file name
                image_file_name = f"{os.path.splitext(filename)[0]}.png"
                image_file_path = os.path.join(images_dir, image_file_name)
                if os.path.exists(image_file_path):
                    print(f"Removing corresponding image: {image_file_path}")
                    os.remove(image_file_path)  # Remove the corresponding image file
                else:
                    print(f"Image file does not exist: {image_file_path}")

def rename_roboflow_files(dataset_source_path):
    # Define the parts of the path
    subdirs = ['train', 'val']
    types = ['images', 'labels']

    for subdir in subdirs:
        for type_ in types:
            # Construct the directory path
            dir_path = os.path.join(dataset_source_path, type_, subdir)

            # Rename each file in the directory
            for filename in os.listdir(dir_path):
                # Check if the filename contains the unnecessary string
                if '.rf.' in filename:
                    # Split the filename at '.rf.' and take the first part
                    new_name = filename.split('.rf.')[0]
                    # Append the correct file extension based on the type
                    new_name += '.png' if type_ == 'images' else '.txt'

                    # Construct the full old and new file paths
                    old_file_path = os.path.join(dir_path, filename)
                    new_file_path = os.path.join(dir_path, new_name)

                    # Rename the file
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed '{filename}' to '{new_name}'")

#This class goes through a YOLO dataset, parses the yaml file, gets the class colors and dict
def normalize_dataset(dataset_source_path, dataset_target_path):
    print("Normalize dataset")
    source_classes_color = {}
    source_classes_id = {}
    for filename in os.listdir(dataset_source_path):
        name, extension = os.path.splitext(filename)
        if extension == '.yaml':
            source_classes_color, source_classes_id = parse_yaml(f'{dataset_source_path}/{filename}')

    path_to_img_folders = f'{dataset_source_path}/{"images"}'
    path_to_lbl_folders = f'{dataset_source_path}/{"labels"}'
    #Iterating through images
    for subfolder in os.listdir(path_to_img_folders):
        path_to_img = f'{path_to_img_folders}/{subfolder}'
        path_to_lbl = f'{path_to_lbl_folders}/{subfolder}'
        for img_file in os.listdir(path_to_img):
            ann_file = img_file.replace('.png', '.txt')
            with open (f'{path_to_lbl}/{ann_file}', 'r') as file:
                annotations = file.readlines()
                new_annotations = []
                for ann in annotations:
                    source_id = int(ann.split()[0])
                    class_name = source_classes_id[source_id]
                    print(class_name)
                    if class_name in classes_id:
                        new_ann = ann.replace(str(source_id), str(classes_id[class_name]))
                        new_annotations.append(new_ann)

            #If there are valid annotations left, copy image and annotation
            if new_annotations:
                path_to_new_img_folders= f'{dataset_target_path}/{"images"}'
                path_to_new_lbl_folders = f'{dataset_target_path}/{"labels"}'
                path_to_new_img = f'{path_to_new_img_folders}/{subfolder}'
                path_to_new_lbl = f'{path_to_new_lbl_folders}/{subfolder}'

                #Checking if folders and subfolders exist for the new dataset
                ensure_directory_exists(f'{dataset_target_path}')
                ensure_directory_exists(path_to_new_img_folders)
                ensure_directory_exists(path_to_new_img)
                ensure_directory_exists(path_to_new_lbl_folders)
                ensure_directory_exists(path_to_new_lbl)

                with open(f'{path_to_new_lbl_folders}/{subfolder}/{ann_file}', 'w') as new_file:
                    new_file.writelines(new_annotations)
                shutil.copy(f'{path_to_img}/{img_file}', f'{path_to_new_img}/{img_file}')
# Uses member variable yaml_path and extracts information from data_config.yaml
# Returns dict of id-classname tuples (Ex: 0:pliers, 1:cup, 2:pen...)
def parse_yaml(yaml_file):
    print("Parsing YAML")
    classes_color = {}
    classes_id = {}
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    for idx, name in enumerate(data['names']):
        classes_color[name] = data['colors'][idx]
        classes_id[idx] = name
    return classes_color, classes_id
# Function to create a folder if it doesn't exist

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)




def copy_corresponding_depth_files(dataset_root_path, dataset_depth_path):
    # Define the subfolders to process
    subfolders = ['train', 'val']

    # Loop through the subfolders (train and val)
    for subfolder in subfolders:
        image_subfolder_path = os.path.join(dataset_root_path, 'images', subfolder)
        depth_target_subfolder_path = os.path.join(dataset_root_path, 'depth', subfolder)

        # Ensure the depth subfolders exist
        if not os.path.exists(depth_target_subfolder_path):
            os.makedirs(depth_target_subfolder_path)

        for image_filename in os.listdir(image_subfolder_path):
            # Extract the timestamp using regex
            timestamp_match = re.search(r"(\d{13,})\.png", image_filename)
            if timestamp_match:
                timestamp = timestamp_match.group(1)

                # Form the corresponding depth image filename and its full path
                depth_filename = f"{timestamp}.tif"
                depth_image_path = os.path.join(dataset_depth_path, depth_filename)

                # Check if the depth image exists and copy it to the target folder
                if os.path.exists(depth_image_path):
                    target_depth_image_path = os.path.join(depth_target_subfolder_path, depth_filename)
                    shutil.copy2(depth_image_path, target_depth_image_path)
                    print(f"Copied {depth_image_path} to {target_depth_image_path}")

def rename_depth_tif(folder_path):
    for filename in os.listdir(folder_path):
        # Use regex to extract the timestamp from the filename
        # This regex now matches both patterns
        timestamp_match = re.search(r"(\d{13,})(?:lt_cloud|_pv_aligned_and_scaled_lt)\.tif", filename)

        if timestamp_match:
            timestamp = timestamp_match.group(1)
            new_filename = f"{timestamp}.tif"

            # Construct full source and target paths
            source_path = os.path.join(folder_path, filename)
            target_path = os.path.join(folder_path, new_filename)

            # Rename the file
            os.rename(source_path, target_path)
            print(f"Renamed {source_path} to {target_path}")

def rename_files_in_subfolder_loop(dataset_source_path):
    # Rename image files
    for subfolder in ['train', 'val']:
        image_path = os.path.join(dataset_source_path, 'images', subfolder)
        rename_files_in_subfolder(image_path, 'png')

    # Rename label files
    for subfolder in ['train', 'val']:
        label_path = os.path.join(dataset_source_path, 'labels', subfolder)
        rename_files_in_subfolder(label_path, 'txt')

def rename_files_in_subfolder(folder_path, extension):
    for filename in os.listdir(folder_path):
        # Use regex to extract the timestamp from the filename
        timestamp_match = re.search(r"(?:train_microDataset_|train_SampleMeshDataset_)(\d{13,})_", filename)

        if timestamp_match:
            timestamp = timestamp_match.group(1)
            new_filename = f"{timestamp}.{extension}"

            # Construct full source and target paths
            source_path = os.path.join(folder_path, filename)
            target_path = os.path.join(folder_path, new_filename)

            # Rename the file
            os.rename(source_path, target_path)
            print(f"Renamed {source_path} to {target_path}")

def rename_files(directory):
    for filename in os.listdir(directory):
        # Check if the filename contains the specific substring and ends with '.tif'
        if "_pv_aligned_and_scaled_lt.tif" in filename:
            # Construct new filename by replacing the substring
            new_filename = filename.replace("_pv_aligned_and_scaled_lt", "lt_cloud")
            # Construct full source and target paths
            source_path = os.path.join(directory, filename)
            target_path = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(source_path, target_path)
            print(f"Renamed {source_path} to {target_path}")

def move_depth_images(dataset_source_path, dataset_target_path):
    # Ensure the target directory exists
    if not os.path.exists(dataset_target_path):
        os.makedirs(dataset_target_path)

    # Walk through every folder and subfolder in the source directory
    for dirpath, _, filenames in os.walk(dataset_source_path):
        # Check if the current directory is a "RawImages" subfolder
        if os.path.basename(dirpath) == "RawImages":
            for filename in filenames:
                if filename.endswith('.tif'):
                    source_file_path = os.path.join(dirpath, filename)
                    target_file_path = os.path.join(dataset_target_path, filename)

                    # Check if a file with the same name already exists in the target directory
                    counter = 1
                    while os.path.exists(target_file_path):
                        name, ext = os.path.splitext(filename)
                        target_file_path = os.path.join(dataset_target_path, f"{name}_{counter}{ext}")
                        counter += 1

                    shutil.copy2(source_file_path, target_file_path)
                    print(f"Copied {source_file_path} to {target_file_path}")


import os


def clean_unannotated_images(dataset_path):
    for subdir in ['train', 'val']:
        images_path = os.path.join(dataset_path, 'images', subdir)
        labels_path = os.path.join(dataset_path, 'labels', subdir)

        # Loop through all image files
        for image_file in os.listdir(images_path):
            if image_file.endswith(".png"):  # Adjust if your images have a different extension
                # Get the base filename without the extension
                base_name = os.path.splitext(image_file)[0]

                # Construct the corresponding annotation file path
                annotation_file = f"{base_name}.txt"
                annotation_path = os.path.join(labels_path, annotation_file)

                # Check if the annotation file exists
                if not os.path.exists(annotation_path):
                    # If the annotation file does not exist, remove the image
                    image_path = os.path.join(images_path, image_file)
                    os.remove(image_path)
                    print(f"Removed unannotated image: {image_path}")

    print("Clean-up of unannotated images is complete.")


if __name__ == '__main__':
    # clean_unannotated_images(dataset_source_path)
    # split_train_val_dataset(dataset_source_path, 0.15)
    resize_images_and_copy_annotations(dataset_source_path, dataset_target_path, new_size=(640, 360))
    # remove_empty_annotations_and_images(dataset_source_path)
    # rename_roboflow_files(dataset_source_path)

