import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms, models

# Set seed for reproducibility
torch.manual_seed(42)

class CropDiseaseMobileNetV2(nn.Module):
    def __init__(self, num_classes=6):
        super().__init__()
        # Load MobileNetV2 pretrained on ImageNet
        self.base = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
        in_features = self.base.classifier[1].in_features # 1280
        
        # Replace classifier head with Identity
        self.base.classifier = nn.Identity()
        
        # Add custom classification head
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        features = self.base(x)
        logits = self.classifier(features)
        return logits

def get_transforms():
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return train_transform, val_transform

def train_model(data_dir="../dataset/color", save_path="../models/crop_disease_model.pth"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using compute device: {device}")
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    train_transform, val_transform = get_transforms()
    
    full_dataset = datasets.ImageFolder(root=data_dir, transform=train_transform)
    num_classes = len(full_dataset.classes)
    
    print("\nClass Indices Mapping (From Dataset Folders):")
    for idx, cls_name in enumerate(full_dataset.classes):
        print(f"  [{idx}] -> {cls_name}")
        
    # Split 80% Train, 20% Validation
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])
    val_dataset.dataset.transform = val_transform

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)
    
    model = CropDiseaseMobileNetV2(num_classes=num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    
    # ── Phase 1: Train Classification Head (Frozen Base) ──
    print("\n--- Phase 1: Feature Extraction (Frozen Base) ---")
    for param in model.base.parameters():
        param.requires_grad = False
        
    optimizer = optim.Adam(model.classifier.parameters(), lr=1e-3)
    
    best_acc = 0.0
    for epoch in range(1, 6):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data)
            total += labels.size(0)
            
        train_acc = correct.double() / total
        
        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels.data)
                val_total += labels.size(0)
        val_acc = val_correct.double() / val_total
        print(f"Epoch {epoch:02d}/05 - Loss: {running_loss/total:.4f} - Train Acc: {train_acc:.4f} - Val Acc: {val_acc:.4f}")

    # ── Phase 2: Fine-Tuning Top Base Layers ──
    print("\n--- Phase 2: Fine-Tuning Top Backbone Layers ---")
    for param in model.base.features[14:].parameters():
        param.requires_grad = True
        
    optimizer = optim.Adam(model.parameters(), lr=1e-5)
    
    for epoch in range(1, 11):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data)
            total += labels.size(0)
            
        train_acc = correct.double() / total
        
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels.data)
                val_total += labels.size(0)
        val_acc = val_correct.double() / val_total
        print(f"Epoch {epoch:02d}/10 - Loss: {running_loss/total:.4f} - Train Acc: {train_acc:.4f} - Val Acc: {val_acc:.4f}")
        
        if val_acc >= best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), save_path)

    print(f"\nTraining Complete! Best PyTorch Model Saved to {save_path} (Val Acc: {best_acc*100:.2f}%)")

if __name__ == "__main__":
    train_model()
