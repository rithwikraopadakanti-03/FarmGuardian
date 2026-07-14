import argparse
import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2 # type: ignore
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization # type: ignore
from tensorflow.keras.models import Model # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard # type: ignore
import matplotlib.pyplot as plt
from preprocess import get_data_generators

def build_model(num_classes=38):
    """Builds the MobileNetV2 based model for transfer learning."""
    # Load base model, exclude top layers
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze the base model for phase 1
    base_model.trainable = False
    
    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    return model, base_model

def plot_history(history, save_path="training_history.png"):
    """Plots and saves training history."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Accuracy plot
    ax1.plot(history.history['accuracy'])
    ax1.plot(history.history['val_accuracy'])
    ax1.set_title('Model Accuracy')
    ax1.set_ylabel('Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.legend(['Train', 'Validation'], loc='lower right')
    
    # Loss plot
    ax2.plot(history.history['loss'])
    ax2.plot(history.history['val_loss'])
    ax2.set_title('Model Loss')
    ax2.set_ylabel('Loss')
    ax2.set_xlabel('Epoch')
    ax2.legend(['Train', 'Validation'], loc='upper right')
    
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Training history plot saved to {save_path}")

def train(dataset_path, model_save_path, epochs_phase1=10, epochs_phase2=15):
    # Setup directories
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    print(f"Starting training pipeline...")
    print(f"Dataset path: {dataset_path}")
    
    # 1. Get Data
    train_gen, val_gen = get_data_generators(dataset_path)
    num_classes = len(train_gen.class_indices)
    print(f"Detected {num_classes} classes.")
    
    # 2. Build Model
    model, base_model = build_model(num_classes=num_classes)
    
    # Callbacks
    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True, monitor='val_accuracy'),
        ModelCheckpoint(model_save_path, save_best_only=True, monitor='val_accuracy'),
        ReduceLROnPlateau(factor=0.2, patience=3, monitor='val_loss'),
        TensorBoard(log_dir="./logs")
    ]
    
    # Phase 1: Feature Extraction
    print("\n--- Phase 1: Feature Extraction (Frozen Base) ---")
    model.compile(optimizer=Adam(learning_rate=1e-3), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
                  
    history1 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs_phase1,
        callbacks=callbacks
    )
    
    # Phase 2: Fine-tuning
    print("\n--- Phase 2: Fine-Tuning (Unfrozen Top Layers) ---")
    base_model.trainable = True
    
    # Freeze all layers except the top 50
    for layer in base_model.layers[:-50]:
        layer.trainable = False
        
    # Recompile with lower learning rate
    model.compile(optimizer=Adam(learning_rate=1e-5), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
                  
    history2 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs_phase2,
        initial_epoch=history1.epoch[-1],
        callbacks=callbacks
    )
    
    # Combine histories for plotting
    for k in history1.history.keys():
        history1.history[k].extend(history2.history[k])
        
    plot_history(history1)
    
    print("\nTraining Complete!")
    print(f"Best model saved to {model_save_path}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train FarmGuardian AI Model")
    parser.add_argument("--dataset", type=str, default="../dataset/color", help="Path to PlantVillage dataset")
    parser.add_argument("--save_path", type=str, default="../models/farmguardian_model.h5", help="Path to save model")
    args = parser.parse_args()
    
    try:
        train(args.dataset, args.save_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run python download_dataset.py first and follow the instructions.")
