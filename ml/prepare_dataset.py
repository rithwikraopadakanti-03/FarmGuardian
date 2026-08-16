import os
import json
import random
import numpy as np
from PIL import Image, ImageDraw

CLASSES = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato___Early_blight",
    "Tomato___healthy",
    "Tomato___Late_blight"
]

def generate_synthetic_leaf(class_name, img_size=(224, 224)):
    """
    Generates realistic, distinct leaf images corresponding to each disease class.
    Potato & Tomato leaves have distinct morphological and lesion patterns.
    """
    img = Image.new("RGB", img_size, color=(210, 210, 210)) # Neutral background
    draw = ImageDraw.Draw(img)
    
    # Base leaf shape coordinates
    if "Potato" in class_name:
        # Oval, broader compound leaf
        leaf_box = [30, 20, 194, 204]
        leaf_color = (34, 139, 34) if "healthy" in class_name else (45, 110, 45)
        draw.ellipse(leaf_box, fill=leaf_color, outline=(20, 80, 20), width=2)
        # Veins
        draw.line([112, 30, 112, 195], fill=(20, 90, 20), width=3)
        draw.line([112, 70, 60, 50], fill=(20, 90, 20), width=2)
        draw.line([112, 110, 160, 90], fill=(20, 90, 20), width=2)
        draw.line([112, 150, 70, 130], fill=(20, 90, 20), width=2)
    else:
        # Tomato leaf - serrated lobed leaflet
        leaf_color = (30, 160, 40) if "healthy" in class_name else (40, 120, 35)
        polygon = [
            (112, 15), (145, 45), (130, 65), (170, 95), (140, 115), 
            (160, 155), (125, 165), (112, 200), (99, 165), (64, 155), 
            (84, 115), (54, 95), (94, 65), (79, 45)
        ]
        draw.polygon(polygon, fill=leaf_color, outline=(15, 90, 25))
        # Veins
        draw.line([112, 20, 112, 190], fill=(15, 80, 20), width=3)
        draw.line([112, 60, 140, 45], fill=(15, 80, 20), width=2)
        draw.line([112, 60, 84, 45], fill=(15, 80, 20), width=2)
        draw.line([112, 100, 150, 85], fill=(15, 80, 20), width=2)
        draw.line([112, 100, 74, 85], fill=(15, 80, 20), width=2)

    # Add disease symptoms based on class
    if "Early_blight" in class_name:
        # Concentric rings / dark brown spots with yellow chlorotic halos
        num_spots = random.randint(8, 15)
        for _ in range(num_spots):
            cx = random.randint(60, 160)
            cy = random.randint(40, 160)
            r_outer = random.randint(10, 18)
            r_inner = r_outer - random.randint(3, 5)
            r_core  = max(2, r_inner - random.randint(2, 4))
            
            # Yellow chlorotic halo
            draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=(200, 200, 30))
            # Dark brown lesion ring
            draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=(90, 40, 15))
            # Concentric core
            draw.ellipse([cx - r_core, cy - r_core, cx + r_core, cy + r_core], fill=(40, 20, 10))

    elif "Late_blight" in class_name:
        # Large water-soaked dark brown / black necrotic patches on margins
        num_patches = random.randint(3, 6)
        for _ in range(num_patches):
            cx = random.randint(50, 170)
            cy = random.randint(30, 170)
            rx = random.randint(20, 45)
            ry = random.randint(20, 45)
            # Dark necrotic patch
            draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(65, 30, 10), outline=(30, 15, 5))

    return img

def prepare_dataset(base_dir="../dataset"):
    os.makedirs(base_dir, exist_ok=True)
    color_dir = os.path.join(base_dir, "color")
    os.makedirs(color_dir, exist_ok=True)
    
    print("=" * 60)
    print("Preparing PlantVillage Dataset Directory Structure...")
    print("=" * 60)

    dataset_summary = {}
    
    # Save class_names.json to both backend and ml directories
    class_mapping = {str(i): cls_name for i, cls_name in enumerate(CLASSES)}
    
    backend_class_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "class_names.json")
    ml_class_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "class_names.json")
    
    with open(backend_class_file, "w") as f:
        json.dump(class_mapping, f, indent=2)
    with open(ml_class_file, "w") as f:
        json.dump(class_mapping, f, indent=2)
        
    print(f"Saved class mapping JSON to {backend_class_file} and {ml_class_file}")

    for idx, cls_name in enumerate(CLASSES):
        cls_dir = os.path.join(color_dir, cls_name)
        os.makedirs(cls_dir, exist_ok=True)
        
        # Generate 60 samples per class (total 360 images)
        sample_count = 60
        for i in range(sample_count):
            img = generate_synthetic_leaf(cls_name)
            img.save(os.path.join(cls_dir, f"sample_{i+1:03d}.jpg"))
            
        dataset_summary[cls_name] = sample_count
        print(f"  Class Index {idx} -> {cls_name:30s}: {sample_count} images generated.")

    print("\nDataset Summary:")
    print(json.dumps(dataset_summary, indent=2))
    print(f"\nTotal Dataset Size: {sum(dataset_summary.values())} images across {len(CLASSES)} classes.")
    return color_dir

if __name__ == "__main__":
    prepare_dataset()
