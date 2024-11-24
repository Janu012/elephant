# -*- coding: utf-8 -*-
"""Tensorflow Model Training Elephant.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mZxzwijwHQGUc73pIvuwPOcZ2lrbJwpX
"""

import os
import numpy as np
import keras
from keras import layers
from tensorflow import data as tf_data
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
import tensorflow as tf  # For tf.data
from keras import layers
from tensorflow.keras.layers import RandomFlip, RandomRotation

from google.colab import drive
drive.mount('/content/drive')

DIR = '/content/drive/MyDrive/finalproject/image'

"""# 1. Prerequisites
 Install Required Libraries
"""

!pip install tensorflow numpy matplotlib opencv-python

import os

# Print the current working directory
print("Current working directory:", os.getcwd())

# List the contents of the '/content/' directory to check if the path exists
print("Contents of '/content/':", os.listdir('/content/'))

# Check if the updated path exists
if os.path.exists(DIR):
    # List and print all contents inside the dataset directory
    dir_contents = os.listdir(DIR)
    print(f"Contents of '{DIR}':", dir_contents)

    # Filter only directories to create classes
    classes = [item for item in dir_contents if os.path.isdir(os.path.join(DIR, item))]
    print("Classes:", classes)
else:
    print(f"The directory {DIR} does not exist.")

"""# 2. Load and Preprocess Data
TensorFlow's ImageDataGenerator or image_dataset_from_directory is ideal for loading and preprocessing data
"""

import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory

# Load the dataset
dataset_path = "/content/drive/MyDrive/finalproject/image"
img_height, img_width = 224, 224  # Resize images to a standard size
batch_size = 32

# Create training and validation datasets
train_dataset = image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

val_dataset = image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

"""# 3. Augment Data (Optional)
Augmentation can help improve model performance by generating variations of images.
"""

from tensorflow.keras.layers import RandomFlip, RandomRotation

data_augmentation = tf.keras.Sequential([
    RandomFlip("horizontal"),
    RandomRotation(0.2),
])

"""# 4. Build the Model
Use a pre-trained model (e.g., MobileNetV2 or ResNet) with transfer learning for better accuracy.
"""

from tensorflow.keras import layers, models

# Load a pre-trained model
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,
    weights='imagenet'
)

# Freeze the base model
base_model.trainable = False

# Add custom layers
model = models.Sequential([
    layers.InputLayer(input_shape=(img_height, img_width, 3)), # Add InputLayer to define input shape
    data_augmentation,
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(2, activation='softmax')  # 2 classes: Bees and Wax Moths
])

"""# 5. Compile and Train the Model"""

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=10
)

model.save('my_model.keras')

"""# 6. Evaluate the Model"""

loss, accuracy = model.evaluate(val_dataset)
print(f"Validation Accuracy: {accuracy:.2f}")

"""# 7. Make Predictions
You can make predictions on new images using the trained model


"""

import numpy as np
from tensorflow.keras.utils import load_img, img_to_array

# Load and preprocess an image
img_path = "/content/drive/MyDrive/finalproject/image/elephant/IMG-20240716-WA0015.jpg"
img = load_img(img_path, target_size=(img_height, img_width))
img_array = img_to_array(img) / 255.0  # Normalize pixel values
img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

# Predict the class
predictions = model.predict(img_array)
predicted_class = tf.argmax(predictions[0]).numpy()
class_names = train_dataset.class_names
print(f"Predicted Class: {class_names[predicted_class]}")

"""# 8. (Optional) Improve the Model
Fine-tune the model: Unfreeze some layers of the pre-trained model and retrain.
Add more data: If your dataset is small, consider data augmentation or synthetic data generation.
Use advanced architectures: Try ResNet, Inception, or EfficientNet for higher accuracy.

# 1. Evaluate on the Validation Set
After training the model, use the validation set to check its performance:

Validation Loss: How well the model predicts.
Validation Accuracy: The percentage of correct predictions.
"""

loss, accuracy = model.evaluate(val_dataset)
print(f"Validation Loss: {loss:.4f}")
print(f"Validation Accuracy: {accuracy:.4f}")

"""# 2. Confusion Matrix
A confusion matrix gives detailed insights into the model's predictions:


"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Get true labels and predictions
true_labels = np.concatenate([y for x, y in val_dataset], axis=0)
predicted_labels = np.argmax(model.predict(val_dataset), axis=1)

# Generate the confusion matrix
cm = confusion_matrix(true_labels, predicted_labels, labels=range(len(train_dataset.class_names)))

# Display the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=train_dataset.class_names)
disp.plot(cmap=plt.cm.Blues)
plt.show()

"""# 3. Classification Report
A classification report shows precision, recall, F1-score, and support for each class.
Precision: Accuracy of positive predictions for a class.
Recall: Ability to find all positive samples for a class.
F1-score: Balance between precision and recall.
Support: The number of samples for each class.
"""

from sklearn.metrics import classification_report

# Generate the report
report = classification_report(true_labels, predicted_labels, target_names=train_dataset.class_names)
print(report)

"""# 4. ROC Curve (For Binary Classification)
The Receiver Operating Characteristic (ROC) curve evaluates the model's ability to distinguish between classes.
"""

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Generate probabilities for the positive class
y_probs = model.predict(val_dataset)[:, 1]  # Assuming class 1 is the positive class
fpr, tpr, thresholds = roc_curve(true_labels, y_probs)
roc_auc = auc(fpr, tpr)

# Plot the ROC curve
plt.figure()
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], 'k--')  # Diagonal line for random guessing
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic")
plt.legend(loc="lower right")
plt.show()

"""# 5. Cross-Validation (Optional)
For robust evaluation, use k-fold cross-validation to train and evaluate the model on different splits of the dataset.

# 6. Visualize Model Predictions
Visualize some predictions to understand where the model performs well or struggles:
"""

import random

# Display sample predictions
plt.figure(figsize=(10, 10))
for images, labels in val_dataset.take(1):
    for i in range(9):  # Display 9 images
        ax = plt.subplot(3, 3, i + 1)
        img = images[i].numpy().astype("uint8")
        label = train_dataset.class_names[labels[i]]
        pred = train_dataset.class_names[np.argmax(model.predict(tf.expand_dims(images[i], axis=0)))]
        plt.imshow(img)
        plt.title(f"True: {label}\nPred: {pred}")
        plt.axis("off")
plt.show()

"""# 7. Metrics for Imbalanced Datasets
If your dataset has unequal samples for each class:

Use metrics like F1-score, ROC-AUC, and Balanced Accuracy.
Employ class weights in model training:
"""

weight_for_class_0 = 1.0
weight_for_class_1 = 1.0

class_weights = {0: weight_for_class_0, 1: weight_for_class_1}
model.fit(train_dataset, validation_data=val_dataset, class_weight=class_weights, epochs=10)

"""# 8. Save Metrics for Analysis
Store training and validation metrics for further analysis:
"""

# Access metrics from training history
history_dict = history.history
train_loss = history_dict['loss']
val_loss = history_dict['val_loss']
train_accuracy = history_dict['accuracy']
val_accuracy = history_dict['val_accuracy']

# Plot training vs validation metrics
plt.figure(figsize=(12, 6))

# Loss
plt.subplot(1, 2, 1)
plt.plot(train_loss, label='Train Loss')
plt.plot(val_loss, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.title('Loss vs Epochs')

# Accuracy
plt.subplot(1, 2, 2)
plt.plot(train_accuracy, label='Train Accuracy')
plt.plot(val_accuracy, label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Accuracy vs Epochs')

plt.show()

"""# 9. Deployment Readiness
Evaluate if the model performs consistently across unseen data. Test with:

New Data Samples: Ensure predictions generalize.
Edge Cases: Handle blurry or incomplete images well.
"""