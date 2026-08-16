import os
import json
import torch
import torch.nn as nn
import onnx
import onnxruntime as ort
import numpy as np
from train_pytorch import CropDiseaseMobileNetV2

class ExportableCropModel(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.model = base_model

    def forward(self, x):
        logits = self.model(x)
        return torch.softmax(logits, dim=1)

def export_to_onnx(model_path="../models/crop_disease_model.pth", output_onnx="../backend/crop_disease_model.onnx"):
    device = torch.device("cpu")
    print(f"Loading trained PyTorch model weights from {model_path}...")
    
    # Load class names
    class_json = "../backend/class_names.json"
    num_classes = 6
    if os.path.exists(class_json):
        with open(class_json, "r") as f:
            classes = json.load(f)
            num_classes = len(classes)
            
    py_model = CropDiseaseMobileNetV2(num_classes=num_classes)
    py_model.load_state_dict(torch.load(model_path, map_location=device))
    py_model.eval()
    
    export_model = ExportableCropModel(py_model)
    export_model.eval()
    
    os.makedirs(os.path.dirname(output_onnx), exist_ok=True)
    
    dummy_input = torch.randn(1, 3, 224, 224, dtype=torch.float32)
    
    print(f"Exporting PyTorch model to ONNX: {output_onnx}...")
    torch.onnx.export(
        export_model,
        dummy_input,
        output_onnx,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}},
        opset_version=14,
        dynamo=False
    )
    
    # Save as self-contained single file
    model_proto = onnx.load(output_onnx)
    onnx.save_model(model_proto, output_onnx, save_as_external_data=False)
    print(f"Successfully exported single-file ONNX model! (Size: {os.path.getsize(output_onnx)/(1024*1024):.2f} MB)")
    
    # Verify ONNX model with onnxruntime
    session = ort.InferenceSession(output_onnx)
    inp_name = session.get_inputs()[0].name
    out = session.run(None, {inp_name: dummy_input.numpy()})[0][0]
    print(f"ONNX Model Output Softmax Probabilities Sum: {np.sum(out):.4f}")
    print(f"ONNX Test Prediction Probabilities: {np.round(out, 4)}")

if __name__ == "__main__":
    export_to_onnx()
