import os
import h5py
import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models

class CropDiseaseModel(nn.Module):
    def __init__(self, weights_path):
        super().__init__()
        # Load MobileNetV2 base model with ImageNet pre-trained weights
        self.base = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
        in_features = self.base.classifier[1].in_features # 1280
        
        self.base.classifier = nn.Identity()
        self.dropout = nn.Dropout(0.3)
        self.fc1 = nn.Linear(in_features, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 6)
        
        # Load trained weights from model.weights.h5
        if os.path.exists(weights_path):
            with h5py.File(weights_path, 'r') as f:
                w1 = f['layers/dense/vars/0'][:]       # (1280, 128)
                b1 = f['layers/dense/vars/1'][:]       # (128,)
                w2 = f['layers/dense_1/vars/0'][:]     # (128, 6)
                b2 = f['layers/dense_1/vars/1'][:]     # (6,)
                
                # PyTorch Linear weight shape is (out_features, in_features)
                self.fc1.weight.data = torch.from_numpy(w1.T).float()
                self.fc1.bias.data = torch.from_numpy(b1).float()
                self.fc2.weight.data = torch.from_numpy(w2.T).float()
                self.fc2.bias.data = torch.from_numpy(b2).float()
                print("Loaded custom trained classification weights into PyTorch model!")

    def forward(self, x):
        # Rescale input RGB image [0..255] to [0.0, 1.0] range matching Keras model config.json Rescaling(1./255)
        x = x / 255.0
        features = self.base(x)
        x = self.dropout(features)
        x = self.fc1(x)
        x = self.relu(x)
        out = self.fc2(x)
        return torch.softmax(out, dim=1)

if __name__ == '__main__':
    weights_h5 = 'backend/model.weights.h5'
    output_onnx = 'backend/crop_disease_model.onnx'
    
    print("Exporting Crop Disease Model to ONNX...")
    model = CropDiseaseModel(weights_h5)
    model.eval()
    
    dummy_input = torch.randn(1, 3, 224, 224)
    torch.onnx.export(
        model,
        dummy_input,
        output_onnx,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}},
        opset_version=18
    )
    import onnx
    m_proto = onnx.load(output_onnx)
    onnx.save_model(m_proto, output_onnx, save_as_external_data=False)
    print(f"Successfully exported single-file ONNX model to {output_onnx} (size: {os.path.getsize(output_onnx)/(1024*1024):.2f} MB)")
