import os
import shutil


source_dir = "../datasets/stock_patterns/ds1/"
destination_dir = "../datasets/stock_patterns/ds1_cleaned/"


# Function to create a folder if it doesn't exist
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def clean_data(subfolder):
    img_subfolder = os.path.join(source_dir, 'images', subfolder)
    label_subfolder = os.path.join(source_dir, 'labels', subfolder)

    # Ensure destination subdirectories exist
    ensure_directory_exists(os.path.join(destination_dir, 'images'))
    ensure_directory_exists(os.path.join(destination_dir, 'labels'))
    ensure_directory_exists(os.path.join(destination_dir, 'images', subfolder))
    ensure_directory_exists(os.path.join(destination_dir, 'labels', subfolder))


    for img_file in os.listdir(img_subfolder):
        # Assuming the image files are either in jpg or png format. Adjust if different.
        if img_file.endswith('.jpg') or img_file.endswith('.png'):
            # Determine the base filename without extension to look up the corresponding label
            base_filename, _ = os.path.splitext(img_file)
            label_file = os.path.join(label_subfolder, base_filename + '.txt')

            # Check if the label file exists and is not empty
            if os.path.exists(label_file) and os.path.getsize(label_file) > 0:
                # Copy image and label to destination folder
                shutil.copy(os.path.join(img_subfolder, img_file),
                            os.path.join(destination_dir, 'images', subfolder, img_file))
                shutil.copy(label_file, os.path.join(destination_dir, 'labels', subfolder, base_filename + '.txt'))


def transfer_val_images(yolo_root_folder):
    # Define paths
    label_val_folder = os.path.join(yolo_root_folder, "labels", "val")
    image_train_folder = os.path.join(yolo_root_folder, "images", "train")
    image_val_folder = os.path.join(yolo_root_folder, "images", "val")

    # Ensure the image validation folder exists
    if not os.path.exists(image_val_folder):
        os.makedirs(image_val_folder)

    # Iterate over each label file in the validation folder
    for label_file in os.listdir(label_val_folder):
        # Construct the image file name (assuming the images are in .jpg format)
        image_name = label_file.replace(".txt", ".png")
        src_path = os.path.join(image_train_folder, image_name)
        dest_path = os.path.join(image_val_folder, image_name)

        # Check if the image exists in the train folder
        if os.path.exists(src_path):
            # Copy the image to the validation folder
            shutil.copy2(src_path, dest_path)
            # Delete the image from the train folder
            os.remove(src_path)



def main():
    transfer_val_images(destination_dir)
    # Copy yaml config file
    # shutil.copy(os.path.join(source_dir, 'data_config.yaml'), destination_dir)
    #
    # # Process train and val subfolders
    # clean_data('train')
    # clean_data('val')

if __name__ == "__main__":
    main()