'''
This script recovers data from Yahoo Finance for all the stocks in stock_names, runs a Yolo inference, and
'''

import os
from ultralytics import YOLO
import shutil

#custom imports
import BoundingBox2D as bb2d
from Frame import Frame

yolo_weights = "./yolo/weights/yoloL_90_3p.pt"
pred_folder = "pred"

class YoloDetector:
    # Setting paths to Yolo results
    results_base_path = './RealTimeResults/'

    def __init__(self, save_predicted_imgs):
        # Initialize the attributes of the class
        self.model = YOLO(yolo_weights)
        #If True, images with predicted bounding boxes will be saved
        self.save_predicted_imgs = save_predicted_imgs
        #Supported patterns, depends on the Yolo weights used
        self.classes_dict = {}
        #Subfolder containing results at each yolo call (typically "pred", incremented in "pred1", "pred2"...)
        self.pred_folder = pred_folder


    def detect_patterns_on_image(self, frame):
        #Setting the path where the predictions will be stored
        results_path = f'{self.results_base_path}/{frame.stock_name}/'

        #Running prediction on the image associated with the frame
        results = self.model.predict(source=frame.img_path, project=results_path, name=self.pred_folder, save=True,
                                     save_txt=True)


        #Setting classes_dict for the first prediction
        if self.classes_dict=={}:
            for id in results[0].names:
                self.classes_dict[id]=results[0].names[id]
            print(f'Retrieved supported Yolo classes: {self.classes_dict}')
        save_dir = results[0].save_dir
        #TODO: extract pattern confidence
        print(results[0])

        bounding_boxes = self.parse_predictions(save_dir)
        if(len(bounding_boxes)==0):
            #Case when no patterns are detected
            print("No patterns have been detected")
        else:
            print("Patterns have been detected")
            #If patterns are detected, convert BoundingBox2D to Patterns and add them to the Frame
            frame.convert_bb2d_to_patterns(bounding_boxes)


    def parse_predictions(self, save_dir):
        print("Parsing predicted results and creating BoundingBox2D objects")
        bounding_boxes = []
        save_dir = save_dir + "/labels/"
        print(save_dir)
        # pred_labels_path = self.project_path + self.pred_folder + '/labels/'
        print(f'Pred labels path : {save_dir}')

        # Parse every single .txt file in the last 'pred' folder
        for filename in os.listdir(save_dir):
            print(filename)
            if filename.endswith('.txt'):
                with open(os.path.join(save_dir, filename), 'r') as file:
                    for line in file:
                        print("Parsing the annotation")
                        # Parse the annotation
                        values = line.split()
                        class_id = int(values[0])
                        x_center, y_center, width, height = map(float, values[1:])
                        bb = bb2d.BoundingBox2D(x_center, y_center, width, height,
                                                str(self.classes_dict[int(class_id)]))
                        bounding_boxes.append(bb)
                        print(bb.box_center)
                        print(bb.box_size)
                        print(bb.name)
        return bounding_boxes
        # Delete the "pred" folders
        # Define the path to the 'pred' folder
        # pred_folder_path = os.path.join(self.project_path, self.pred_folder)

        # Delete the "pred" folder
        # shutil.rmtree(pred_folder_path)

        # # Step 3: Copy the .txt files to a "results" folder and delete the "predN" folders
        # results_folder = os.path.join(project_path, "results")
        # os.makedirs(results_folder, exist_ok=True)

        # # Copy the .txt files
        # for filename in os.listdir(last_pred_folder_path):
        #     if filename.endswith('.txt'):
        #         shutil.copy2(os.path.join(last_pred_folder_path, filename), results_folder)




