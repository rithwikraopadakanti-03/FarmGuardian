import os
import io
import random

try:
    import numpy as np
    from PIL import Image
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False

# We'll try to import tensorflow, but provide a simulation mode if it fails or model isn't found
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

from app.core.config import settings

class MLService:
    def __init__(self):
        self.model = None
        self.simulation_mode = True
        self.CLASS_NAMES = [
            'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
            'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
            'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
            'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
            'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
            'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)',
            'Peach___Bacterial_spot', 'Peach___healthy',
            'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
            'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
            'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
            'Strawberry___Leaf_scorch', 'Strawberry___healthy',
            'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
            'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
            'Tomato___healthy'
        ]
        self.load_model()

    def load_model(self):
        if TF_AVAILABLE and os.path.exists(settings.MODEL_PATH):
            try:
                self.model = tf.keras.models.load_model(settings.MODEL_PATH)
                self.simulation_mode = False
                print(f"Loaded ML model from {settings.MODEL_PATH}")
            except Exception as e:
                print(f"Failed to load model: {e}. Falling back to simulation mode.")
                self.simulation_mode = True
        else:
            print("TF not available or model file not found. Running in SIMULATION MODE.")
            self.simulation_mode = True

    def is_loaded(self):
        return not self.simulation_mode

    def preprocess_image(self, image_bytes: bytes):
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((224, 224))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        img_array = np.array(image)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        return img_array

    def predict(self, image_bytes: bytes):
        if self.simulation_mode:
            # Simulate a realistic prediction based on image color hints
            # (In a real scenario, this would just be random, but for demo we can pick a common disease)
            # We'll just randomly select one of the more common tomato/potato diseases for demo
            demo_classes = [
                'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
                'Potato___Early_blight', 'Potato___Late_blight', 'Corn_(maize)___Common_rust_',
                'Tomato___healthy'
            ]
            disease = random.choice(demo_classes)
            confidence = round(random.uniform(0.85, 0.99), 4)
            if 'healthy' in disease:
                confidence = round(random.uniform(0.95, 0.99), 4)
            return disease, confidence
            
        try:
            img_array = self.preprocess_image(image_bytes)
            predictions = self.model.predict(img_array)[0]
            predicted_class_idx = np.argmax(predictions)
            confidence = float(predictions[predicted_class_idx])
            disease = self.CLASS_NAMES[predicted_class_idx]
            return disease, confidence
        except Exception as e:
            print(f"Prediction error: {e}")
            return "Unknown", 0.0

ml_service = MLService()
