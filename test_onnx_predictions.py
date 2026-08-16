import os
import json
import numpy as np
import onnxruntime as ort
from PIL import Image, ImageDraw
import io

def create_sample_leaf(class_name):
    img = Image.new("RGB", (224, 224), color=(210, 210, 210))
    draw = ImageDraw.Draw(img)
    
    if "Potato" in class_name:
        leaf_box = [30, 20, 194, 204]
        leaf_color = (34, 139, 34) if "healthy" in class_name else (45, 110, 45)
        draw.ellipse(leaf_box, fill=leaf_color, outline=(20, 80, 20), width=2)
    else:
        leaf_color = (30, 160, 40) if "healthy" in class_name else (40, 120, 35)
        polygon = [(112, 15), (145, 45), (130, 65), (170, 95), (140, 115), (160, 155), (125, 165), (112, 200), (99, 165), (64, 155), (84, 115), (54, 95), (94, 65), (79, 45)]
        draw.polygon(polygon, fill=leaf_color, outline=(15, 90, 25))

    if "Early_blight" in class_name:
        for _ in range(12):
            cx, cy = np.random.randint(60, 160), np.random.randint(40, 160)
            draw.ellipse([cx-15, cy-15, cx+15, cy+15], fill=(200, 200, 30))
            draw.ellipse([cx-10, cy-10, cx+10, cy+10], fill=(90, 40, 15))
    elif "Late_blight" in class_name:
        for _ in range(4):
            cx, cy = np.random.randint(50, 170), np.random.randint(30, 170)
            draw.ellipse([cx-35, cy-35, cx+35, cy+35], fill=(65, 30, 10))
            
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_inference():
    onnx_path = "backend/crop_disease_model.onnx"
    class_path = "backend/class_names.json"
    
    session = ort.InferenceSession(onnx_path)
    with open(class_path, "r") as f:
        class_mapping = json.load(f)
        
    print("=" * 60)
    print("        INFERENCE TEST REPORT (REAL ONNX MODEL)")
    print("=" * 60)

    test_classes = [
        "Tomato___Early_blight",
        "Tomato___healthy",
        "Tomato___Late_blight",
        "Potato___Early_blight",
        "Potato___healthy",
        "Potato___Late_blight"
    ]

    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std  = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    for target_cls in test_classes:
        img_bytes = create_sample_leaf(target_cls)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((224, 224))
        raw_arr = np.array(img, dtype=np.float32) / 255.0
        norm_arr = (raw_arr - mean) / std
        inp_tensor = np.expand_dims(np.transpose(norm_arr, (2, 0, 1)), axis=0).astype(np.float32)

        input_name = session.get_inputs()[0].name
        probs = session.run(None, {input_name: inp_tensor})[0][0]
        
        top_idx = int(np.argmax(probs))
        top_cls = class_mapping[str(top_idx)]
        conf = probs[top_idx]
        
        top_3_indices = np.argsort(probs)[::-1][:3]
        
        print(f"\nTarget Input: {target_cls}")
        print(f"Prediction  : {top_cls} (Confidence: {conf*100:.2f}%)")
        print("Top 3 Predictions:")
        for rank, idx in enumerate(top_3_indices, 1):
            print(f"  {rank}. {class_mapping[str(idx)]:25s} – {probs[idx]*100:.2f}%")

if __name__ == "__main__":
    test_inference()
