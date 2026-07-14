import argparse
import tensorflow as tf
import os
import json

def export_to_tflite(model_path, output_path):
    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    
    print("Converting to TFLite (FP16 Quantization)...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Enable optimizations for mobile
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # Float16 quantization to reduce size by half with minimal accuracy loss
    converter.target_spec.supported_types = [tf.float16]
    
    tflite_model = converter.convert()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
        
    print(f"TFLite model saved to {output_path}")
    
    # Compare sizes
    h5_size = os.path.getsize(model_path) / (1024 * 1024)
    tflite_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\nSize Comparison:")
    print(f"Original .h5:  {h5_size:.2f} MB")
    print(f"TFLite (.tflite): {tflite_size:.2f} MB")
    print(f"Reduction: {(1 - tflite_size/h5_size)*100:.1f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export FarmGuardian Model")
    parser.add_argument("--model", type=str, default="../models/farmguardian_model.h5")
    parser.add_argument("--output", type=str, default="../models/farmguardian_model.tflite")
    args = parser.parse_args()
    
    try:
        export_to_tflite(args.model, args.output)
    except Exception as e:
        print(f"Export error: {e}")
