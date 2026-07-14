import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore
import os

def get_data_generators(dataset_path, img_size=(224, 224), batch_size=32):
    """
    Creates and returns training and validation data generators with augmentation.
    """
    # Verify dataset exists
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset path {dataset_path} does not exist. Please download it first.")
        
    print(f"Loading dataset from {dataset_path}...")
    
    # We use validation_split to automatically split the dataset
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2 # 80% train, 20% validation
    )
    
    # No augmentation for validation, just rescale
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    train_generator = datagen.flow_from_directory(
        dataset_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    validation_generator = val_datagen.flow_from_directory(
        dataset_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    print("\nClass Indices Mapping:")
    print(train_generator.class_indices)
    
    return train_generator, validation_generator

if __name__ == "__main__":
    print("Testing Preprocessing Pipeline...")
    # This assumes dataset is at ../dataset/color
    try:
        train_gen, val_gen = get_data_generators("../dataset/color")
        print(f"Train batches: {len(train_gen)}")
        print(f"Validation batches: {len(val_gen)}")
    except Exception as e:
        print(f"Error: {e}")
