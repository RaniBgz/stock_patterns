import os
import shutil
import re
from ultralytics import YOLO


weight_path = "D:/Freelance/stock_patterns/yolo/weights/dbdths/dbdths_v1.pt"
# images_path = "D:/Freelance/stock_patterns/datasets/inference/inference_sample/images/"
dataset_path ="D:/Freelance/stock_patterns/datasets/inference/inference_dataset_sept2023_2m/"
images_path = f"{dataset_path}/images/train/"
target_labels_path = f"{dataset_path}/labels/train/"
yolo_inference_path = "D:/Freelance/stock_patterns/runs/detect/"
#Save path seems to be ./runs/detect/predict


def recognize_patterns_batch(images_path=''):
    print(f"Recognizing patterns on batch of data located at {images_path}")
    model = YOLO(weight_path)

    # List all files in images_path
    image_files = [f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f)) and f.endswith(('.jpg', '.jpeg', '.png'))]

    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)

        # Predict
        model.predict(image_path, save=True, device=0, save_txt=True, imgsz=(720, 1280), conf=0.3)

        # # Assuming output files have the same name but different extensions
        # # Move image and txt outputs to the desired folders
        # output_image = image_path.replace('.jpg', '.png')  # Adjust the extension as per your need
        # output_txt = image_path.replace('.jpg', '.txt')
        #
        # # Check if they exist and move
        # if os.path.exists(output_image):
        #     os.rename(output_image, os.path.join(output_images_path, image_file.replace('.jpg', '.png')))
        # if os.path.exists(output_txt):
        #     os.rename(output_txt, os.path.join(output_txt_path, image_file.replace('.jpg', '.txt')))


def populate_dataset_structure(images_path, dataset_path):
    # Ensure the output folders exist
    os.makedirs(os.path.join(dataset_path, "images/train"), exist_ok=True)
    os.makedirs(os.path.join(dataset_path, "labels/train"), exist_ok=True)

    # Iterate over all files in the images_path
    for filename in os.listdir(images_path):
        # Check if the file is an image (based on extension, you can expand this list)
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            # Copy image to dataset_path + "images/train/"
            shutil.copy(os.path.join(images_path, filename), os.path.join(dataset_path, "images/train", filename))

            # Create an empty annotation .txt file
            annotation_filename = os.path.splitext(filename)[0] + '.txt'
            with open(os.path.join(dataset_path, "labels/train", annotation_filename), 'w') as f:
                pass  # Empty file is created

def create_empty_labels(dataset_path):
    # Ensure the output folders exist
    images_path = f"{dataset_path}/images/train/"
    labels_path = f"{dataset_path}/labels/train/"

    # Ensure that the labels directory exists
    if not os.path.exists(labels_path):
        os.makedirs(labels_path)

    # Loop through all image files
    for img_file in os.listdir(images_path):
        # Check if the file is an image (e.g., ends with ".png")
        if img_file.endswith(".png"):
            # Determine the base filename without the extension
            base_name = os.path.splitext(img_file)[0]

            # Create a corresponding empty .txt file in the labels_path directory
            empty_label_path = os.path.join(labels_path, f"{base_name}.txt")

            # Create the empty file (by simply opening it in write mode and then closing it)
            with open(empty_label_path, 'w') as _:
                pass

    print("Empty label files created successfully!")


#Copy inference results
def copy_latest_yolo_labels(yolo_inference_path, target_labels_path):
    # List all subdirectories in yolo_inference_path
    all_subdirs = [d for d in os.listdir(yolo_inference_path) if os.path.isdir(os.path.join(yolo_inference_path, d))]

    # Use regular expression to get all X values and find the maximum
    # This approach allows for any number of digits in X
    max_run = max([int(re.search(r'predict(\d+)', d).group(1)) for d in all_subdirs if re.search(r'predict(\d+)', d)])

    # Construct the path to the labels directory of the latest run
    latest_labels_path = os.path.join(yolo_inference_path, f"predict{max_run}", "labels")

    # Copy all .txt files from latest_labels_path to target_labels_path
    for label_file in os.listdir(latest_labels_path):
        if label_file.endswith('.txt'):
            shutil.copy2(os.path.join(latest_labels_path, label_file), os.path.join(target_labels_path, label_file))




if __name__ == "__main__":
    # create_empty_labels(dataset_path)

    # recognize_patterns_batch(images_path)
    copy_latest_yolo_labels(yolo_inference_path, target_labels_path)


    # populate_dataset_structure(images_path, dataset_path)
    #
    # copy_latest_yolo_labels(yolo_inference_path, target_labels_path)




