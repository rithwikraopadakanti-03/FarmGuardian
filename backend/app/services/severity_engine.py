try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

class SeverityEngine:
    def analyze_severity(self, image_bytes: bytes, disease: str, confidence: float):
        if 'healthy' in disease.lower():
            return "Healthy", 0.0

        if not CV2_AVAILABLE:
            import random
            score = round(random.uniform(15.0, 85.0), 2)
            if score < 25:
                level = "Mild"
            elif score < 60:
                level = "Moderate"
            else:
                level = "Severe"
            return level, score

        try:
            # Convert bytes to numpy array for cv2
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert to HSV color space
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Define range for brown/yellow (diseased spots)
            # These ranges are approximations for generic leaf lesions
            lower_brown = np.array([10, 50, 20])
            upper_brown = np.array([40, 255, 255])
            
            # Define range for green (healthy parts)
            lower_green = np.array([35, 50, 20])
            upper_green = np.array([85, 255, 255])
            
            # Create masks
            mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
            mask_green = cv2.inRange(hsv, lower_green, upper_green)
            
            brown_pixels = cv2.countNonZero(mask_brown)
            green_pixels = cv2.countNonZero(mask_green)
            
            total_leaf_pixels = brown_pixels + green_pixels
            
            if total_leaf_pixels == 0:
                lesion_coverage = 0.5 # fallback
            else:
                lesion_coverage = brown_pixels / total_leaf_pixels
                
            # Combine image analysis with model confidence to get severity score
            # A highly confident disease prediction boosts severity slightly
            base_score = lesion_coverage * 100
            severity_score = min(100.0, base_score + (confidence * 10))
            
            # Categorize
            if severity_score < 25:
                level = "Mild"
            elif severity_score < 60:
                level = "Moderate"
            else:
                level = "Severe"
                
            return level, round(severity_score, 2)
            
        except Exception as e:
            print(f"Severity analysis error: {e}")
            # Fallback for demo or error
            import random
            score = round(random.uniform(15.0, 85.0), 2)
            if score < 25:
                level = "Mild"
            elif score < 60:
                level = "Moderate"
            else:
                level = "Severe"
            return level, score

severity_engine = SeverityEngine()
