import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.preprocessing.image import ImageDataGenerator
import os

# --- 1. Dataset Configuration ---
# The path to our NEW, split dataset directory created by prepare_dataset.py
split_data_dir = 'Coconut_Dataset_Split'
train_dir = os.path.join(split_data_dir, 'train')
validation_dir = os.path.join(split_data_dir, 'validation')

# Check if the split dataset directory exists before proceeding
if not os.path.exists(split_data_dir):
    print(f"FATAL ERROR: Split dataset directory not found at '{split_data_dir}'")
    print("Please run the 'prepare_dataset.py' script first to create the split dataset.")
    exit()

# --- 2. Image Data Preparation ---
# Create an ImageDataGenerator for the training data with data augmentation.
# Augmentation creates modified versions of your images, which helps the model generalize better.
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,         # Normalize pixel values from 0-255 to 0-1
    rotation_range=40,         # Randomly rotate images by up to 40 degrees
    width_shift_range=0.2,     # Randomly shift images horizontally
    height_shift_range=0.2,    # Randomly shift images vertically
    shear_range=0.2,           # Apply shearing transformations
    zoom_range=0.2,            # Randomly zoom in on images
    horizontal_flip=True,      # Randomly flip images horizontally
    fill_mode='nearest'        # Strategy for filling in newly created pixels
)

# Create a separate, simpler generator for the validation data.
# We only need to rescale the validation images; no augmentation is needed.
validation_datagen = ImageDataGenerator(rescale=1.0/255.0)

# --- 3. Load Data from Directories ---
# Training data generator: reads images from the 'train' folder
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),    # Resize all images to a consistent 224x224 pixels
    batch_size=32,             # Process images in batches of 32
    class_mode='categorical',  # Use for multi-class classification
    shuffle=True               # Shuffle the training data for better learning
)

# Validation data generator: reads images from the 'validation' folder
validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False              # No need to shuffle validation data
)

# Get the number of classes (disease categories) from the generator
num_classes = len(train_generator.class_indices)
print(f"Found {num_classes} classes: {list(train_generator.class_indices.keys())}")


# --- 4. Define the AI Model (Convolutional Neural Network) ---
model = keras.Sequential([
    # Input Layer and first convolutional block
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    layers.MaxPooling2D(2, 2),

    # Second convolutional block
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    # Third convolutional block
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    # Flatten the 2D feature maps into a 1D vector
    layers.Flatten(),

    # A dense (fully connected) layer for high-level pattern recognition
    layers.Dense(512, activation='relu'),
    # Dropout layer to prevent overfitting by randomly setting a fraction of input units to 0
    layers.Dropout(0.5), 
    
    # Output Layer: produces the final probability for each class
    layers.Dense(num_classes, activation='softmax')
])

# --- 5. Compile the Model ---
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy', # The standard loss function for multi-class classification
    metrics=['accuracy']
)

# Print a summary of the model's architecture
model.summary()

# --- 6. Train the Model ---
print("\nStarting model training with the properly structured dataset...")
history = model.fit(
    train_generator,
    epochs=25, # An epoch is one full pass through the entire training dataset
    validation_data=validation_generator,
    verbose=1
)
print("Model training completed.")

# --- 7. Save the Trained Model ---
# The saved file will be used by app.py to make live predictions.
model.save('coconut_disease_model.h5')
print("\nNew, properly trained model saved as 'coconut_disease_model.h5'")

