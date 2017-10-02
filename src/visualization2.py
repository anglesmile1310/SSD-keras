import random
from datasets import DataManager
# from models.ssd import SSD300
from utils.boxes import create_prior_boxes
from utils.preprocessing import load_image
from utils.inference import plot_box_data
from utils.inference import get_colors
from utils.boxes import assign_prior_boxes
import matplotlib.pyplot as plt


# data manager
# ------------------------------------------------------------------
split = 'train'
dataset_name = 'VOC2007'
dataset_manager = DataManager(dataset_name, split)
ground_truth_data = dataset_manager.load_data()
class_names = dataset_manager.class_names
print('Found:', len(ground_truth_data), 'images')
print('Class names: \n', class_names)


class_names = ['background', 'diningtable', 'chair']
dataset_manager = DataManager(dataset_name, split, class_names)
ground_truth_data = dataset_manager.load_data()
class_names = dataset_manager.class_names
print('Found:', len(ground_truth_data), 'images')
print('Class names: \n', class_names)


# prior boxes
# ------------------------------------------------------------------
# model = SSD300()
prior_boxes = create_prior_boxes()
print('Prior boxes shape:', prior_boxes.shape)
print('Prior box example:', prior_boxes[777])


image_path = '../images/fish-bike.jpg'
# input_shape = model.input_shape[1:3]
input_shape = (300, 300)
image_array = load_image(image_path, input_shape)
box_coordinates = prior_boxes[6010:6020, :]
plot_box_data(box_coordinates, image_array)
plt.imshow(image_array)
plt.show()


# ground truth
# ------------------------------------------------------------------
image_name, box_data = random.sample(ground_truth_data.items(), 1)[0]
print('Data sample: \n', box_data)
image_path = dataset_manager.images_path + image_name
arg_to_class = dataset_manager.arg_to_class
colors = get_colors(len(class_names))
image_array = load_image(image_path, input_shape)
plot_box_data(box_data, image_array, arg_to_class, colors=colors)
plt.imshow(image_array)
plt.show()

assigned_boxes = assign_prior_boxes(prior_boxes, box_data, len(class_names),
                                    regress=False, overlap_threshold=.5)
positive_mask = assigned_boxes[:, 4] != 1
positive_boxes = assigned_boxes[positive_mask]
image_array = load_image(image_path, input_shape)
plot_box_data(positive_boxes, image_array, arg_to_class, colors=colors)
plt.imshow(image_array)
plt.show()


