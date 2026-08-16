import os
import json
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support, accuracy_score
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from train_pytorch import CropDiseaseMobileNetV2

def evaluate_model(model_path="../models/crop_disease_model.pth", data_dir="../dataset/color"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    dataset = datasets.ImageFolder(root=data_dir, transform=val_transform)
    classes = dataset.classes
    loader = DataLoader(dataset, batch_size=16, shuffle=False)
    
    model = CropDiseaseMobileNetV2(num_classes=len(classes)).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    y_true = []
    y_pred = []
    
    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            
            y_true.extend(labels.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())
            
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
    
    print("=" * 60)
    print("      MODEL EVALUATION METRICS REPORT")
    print("=" * 60)
    print(f"  Overall Accuracy : {acc * 100:.2f}%")
    print(f"  Precision (Macro): {precision * 100:.2f}%")
    print(f"  Recall (Macro)   : {recall * 100:.2f}%")
    print(f"  F1-Score (Macro) : {f1 * 100:.2f}%\n")
    
    print("CLASSIFICATION REPORT:")
    print("-" * 60)
    report = classification_report(y_true, y_pred, target_names=classes, digits=4)
    print(report)
    
    cm = confusion_matrix(y_true, y_pred)
    print("\nCONFUSION MATRIX:")
    print("-" * 60)
    print("Classes:")
    for i, c in enumerate(classes):
        print(f"  [{i}] {c}")
    print("\nMatrix (Rows=True, Cols=Predicted):")
    print(cm)
    
    # Save Confusion Matrix Plot
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix - Plant Disease Classifier')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, [c.split('___')[-1] for c in classes], rotation=45)
    plt.yticks(tick_marks, [c.split('___')[-1] for c in classes])
    
    fmt = 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
                     
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    os.makedirs("../docs", exist_ok=True)
    cm_path = "../docs/confusion_matrix.png"
    plt.savefig(cm_path)
    print(f"\nSaved Confusion Matrix Plot to {cm_path}")

if __name__ == "__main__":
    evaluate_model()
