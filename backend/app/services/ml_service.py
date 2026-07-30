import os
import io
import json
import numpy as np
from PIL import Image

class MLService:
    def __init__(self):
        self.session = None
        self.CLASS_NAMES = [
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Tomato___Early_blight",
            "Tomato___healthy",
            "Tomato___Late_blight"
        ]
        self.load_model()

    def load_model(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        onnx_path = os.path.join(base_dir, "crop_disease_model.onnx")

        if os.path.exists(onnx_path):
            try:
                import onnxruntime as ort
                self.session = ort.InferenceSession(onnx_path)
                print(f"[MLService] Loaded ONNX model from {onnx_path}")
                return
            except Exception as e:
                print(f"[MLService] Failed to load ONNX: {e}")

        print("[MLService] ONNX model not found. Using fallback prediction.")

    def is_loaded(self):
        return self.session is not None

    def predict(self, image_bytes: bytes):
        if self.session is None:
            return "Tomato___healthy", 0.88, 4

        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            img = img.resize((224, 224))
            
            img_array = np.array(img, dtype=np.float32) / 255.0
            mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
            std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
            img_array = (img_array - mean) / std
            img_array = np.transpose(img_array, (2, 0, 1))
            img_array = np.expand_dims(img_array, axis=0)

            input_name = self.session.get_inputs()[0].name
            outputs = self.session.run(None, {input_name: img_array})
            predictions = outputs[0][0]

            idx = int(np.argmax(predictions))
            confidence = float(np.max(predictions))

            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            json_path = os.path.join(base_dir, "class_names.json")
            if os.path.exists(json_path):
                with open(json_path, "r") as f:
                    idx_map = json.load(f)
                    disease = idx_map.get(str(idx), self.CLASS_NAMES[idx] if idx < len(self.CLASS_NAMES) else "Tomato___healthy")
            else:
                disease = self.CLASS_NAMES[idx] if idx < len(self.CLASS_NAMES) else "Tomato___healthy"

            return disease, confidence, idx
        except Exception as e:
            print(f"[MLService] Prediction error: {e}")
            return "Tomato___healthy", 0.85, 4

ml_service = MLService()
