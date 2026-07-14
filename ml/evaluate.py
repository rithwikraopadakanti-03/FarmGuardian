import argparse
import tensorflow as tf
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from preprocess import get_data_generators

def evaluate_model(model_path, dataset_path, output_dir="../docs"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    
    # Use validation generator as test set for evaluation
    _, test_gen = get_data_generators(dataset_path, batch_size=32)
    
    print("\nEvaluating model...")
    results = model.evaluate(test_gen)
    print(f"Test Loss: {results[0]:.4f}")
    print(f"Test Accuracy: {results[1]*100:.2f}%")
    
    print("\nGenerating predictions for classification report...")
    # Get true labels and predictions
    y_true = test_gen.classes
    class_names = list(test_gen.class_indices.keys())
    
    # Reset generator before predict
    test_gen.reset()
    y_pred_prob = model.predict(test_gen)
    y_pred = np.argmax(y_pred_prob, axis=1)
    
    # Classification Report
    print("\nClassification Report:")
    report = classification_report(y_true, y_pred, target_names=class_names, output_dict=True)
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    # Save metrics to JSON
    metrics_path = os.path.join(output_dir, "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(report, f, indent=4)
    print(f"Saved metrics to {metrics_path}")
    
    # Confusion Matrix
    print("\nGenerating Confusion Matrix...")
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(20, 20))
    sns.heatmap(cm, annot=False, cmap="Blues", fmt="d", xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=90)
    plt.tight_layout()
    
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_path)
    print(f"Saved confusion matrix plot to {cm_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate FarmGuardian AI Model")
    parser.add_argument("--model", type=str, default="../models/farmguardian_model.h5", help="Path to trained model")
    parser.add_argument("--dataset", type=str, default="../dataset/color", help="Path to dataset for evaluation")
    args = parser.parse_args()
    
    try:
        evaluate_model(args.model, args.dataset)
    except Exception as e:
        print(f"Evaluation error: {e}")
