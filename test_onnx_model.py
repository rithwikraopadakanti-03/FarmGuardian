import json
import numpy as np
import onnxruntime as ort

def test_local_model():
    session = ort.InferenceSession('backend/crop_disease_model.onnx')
    
    # Create green leaf image array
    arr = np.zeros((224, 224, 3), dtype=np.float32)
    arr[:, :, 1] = 160.0 # Green channel
    arr[30:190, 30:190, 1] = 220.0
    arr[80:140, 80:140, 0] = 40.0
    
    # Normalize with ImageNet mean and std
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    norm = ((arr / 255.0) - mean) / std
    
    inp = np.expand_dims(np.transpose(norm, (2, 0, 1)), axis=0)
    
    outputs = session.run(None, {'input': inp})
    probs = outputs[0][0]
    
    with open('backend/class_names.json') as f:
        names = json.load(f)
        
    top_idx = int(np.argmax(probs))
    
    print("--- LOCAL ONNX MODEL TEST RESULT ---")
    print(f"Predicted Index: {top_idx}")
    print(f"Predicted Class: {names[str(top_idx)]}")
    print(f"Confidence:      {probs[top_idx]*100:.2f}%\n")
    print("All Class Probabilities:")
    for i in range(6):
        print(f"  Class {i} [{names[str(i)]}]: {probs[i]*100:.2f}%")

if __name__ == '__main__':
    test_local_model()
