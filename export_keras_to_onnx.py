import os
import h5py
import numpy as np

# We build Keras MobileNetV2 model structure and save to SavedModel / ONNX
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Model

def export_keras_onnx():
    weights_path = 'backend/model.weights.h5'
    output_onnx = 'backend/crop_disease_model.onnx'
    
    print("Building Keras MobileNetV2 model...")
    inputs = Input(shape=(224, 224, 3), name='input_layer')
    # Rescale 0..255 float image to [-1, 1] range for MobileNetV2
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False
    
    features = base_model(x)
    gap = GlobalAveragePooling2D()(features)
    drop = Dropout(0.3)(gap)
    dense1 = Dense(128, activation='relu', name='dense')(drop)
    outputs = Dense(6, activation='softmax', name='dense_1')(dense1)
    
    model = Model(inputs=inputs, outputs=outputs)
    
    # Load custom weights from backend/model.weights.h5
    if os.path.exists(weights_path):
        with h5py.File(weights_path, 'r') as f:
            w1 = f['layers/dense/vars/0'][:]
            b1 = f['layers/dense/vars/1'][:]
            w2 = f['layers/dense_1/vars/0'][:]
            b2 = f['layers/dense_1/vars/1'][:]
            
            model.get_layer('dense').set_weights([w1, b1])
            model.get_layer('dense_1').set_weights([w2, b2])
            print("Loaded custom weights into Keras model!")
            
    # Save temporary SavedModel
    saved_model_dir = 'scratch/saved_model_temp'
    os.makedirs(saved_model_dir, exist_ok=True)
    model.save(saved_model_dir)
    print("Saved Keras model to temp SavedModel directory.")
    
    # Convert SavedModel to ONNX using tf2onnx
    import tf2onnx
    import onnx
    
    print("Converting SavedModel to ONNX using tf2onnx...")
    model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=[tf.TensorSpec((None, 224, 224, 3), tf.float32, name='input')], opset=13)
    
    onnx.save_model(model_proto, output_onnx, save_as_external_data=False)
    print(f"Successfully exported Keras ONNX model to {output_onnx} (size: {os.path.getsize(output_onnx)/(1024*1024):.2f} MB)")

if __name__ == '__main__':
    export_keras_onnx()
