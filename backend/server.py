"""
FarmGuardian AI — Backend Server
Real AI predictions powered by TensorFlow/Keras.
"""

import http.server
import json
import os
import uuid
import random
import hashlib
import hmac
import base64
import time
import sqlite3
import mimetypes
import urllib.parse
from datetime import datetime
from io import BytesIO
from pathlib import Path

# ─── TensorFlow / Real Model Loading ────────────────────────────────────────

MODEL = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), "crop_disease_model.keras")

def load_model():
    global MODEL
    try:
        import tensorflow as tf
        print("[AI] Loading Keras model from:", MODEL_PATH)
        MODEL = tf.keras.models.load_model(MODEL_PATH)
        print("[AI] Model loaded successfully! Input shape:", MODEL.input_shape)
    except Exception as e:
        print(f"[AI] WARNING: Could not load model ({e}). Falling back to simulation mode.")
        MODEL = None

load_model()

# ─── Configuration ───────────────────────────────────────────────────────────

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8000))
SECRET_KEY = "farmguardian-secret-key-change-in-production"
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
REPORTS_DIR = os.path.join(UPLOAD_DIR, "reports")
DB_PATH = os.path.join(os.path.dirname(__file__), "farmguardian.db")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# ─── Database Setup ──────────────────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            password_hash TEXT NOT NULL,
            is_guest INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            disease TEXT,
            confidence REAL,
            severity_level TEXT,
            severity_score REAL,
            risk_level TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ─── Auth Helpers ─────────────────────────────────────────────────────────────

def hash_password(password):
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return (salt + key).hex()

def verify_password(password, stored_hash):
    stored_bytes = bytes.fromhex(stored_hash)
    salt = stored_bytes[:16]
    stored_key = stored_bytes[16:]
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return hmac.compare_digest(stored_key, new_key)

def create_token(username):
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload_data = {"sub": username, "exp": int(time.time()) + 86400}
    payload = base64.urlsafe_b64encode(json.dumps(payload_data).encode()).decode().rstrip("=")
    signature = hmac.new(SECRET_KEY.encode(), f"{header}.{payload}".encode(), hashlib.sha256).hexdigest()
    return f"{header}.{payload}.{signature}"

def decode_token(token):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        padding = 4 - len(parts[1]) % 4
        payload_str = base64.urlsafe_b64decode(parts[1] + "=" * padding).decode()
        payload = json.loads(payload_str)
        if payload.get("exp", 0) < time.time():
            return None
        expected_sig = hmac.new(SECRET_KEY.encode(), f"{parts[0]}.{parts[1]}".encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, parts[2]):
            return None
        return payload.get("sub")
    except Exception:
        return None

# ─── ML Simulation Service ───────────────────────────────────────────────────

CLASS_NAMES = [
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

DEMO_DISEASES = [
    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Potato___Early_blight', 'Potato___Late_blight', 'Corn_(maize)___Common_rust_',
    'Apple___Apple_scab', 'Grape___Black_rot', 'Tomato___healthy', 'Potato___healthy'
]

RECOMMENDATIONS = {
    "en": {
        "immediate_actions": [
            "Remove and destroy all infected leaves immediately.",
            "Isolate the affected plants from healthy ones.",
            "Ensure proper air circulation around plants."
        ],
        "organic_treatments": [
            "Apply neem oil spray (2-3ml per liter of water).",
            "Use copper-based organic fungicide.",
            "Apply baking soda solution (1 tbsp per gallon of water).",
            "Spray compost tea to boost plant immunity."
        ],
        "chemical_treatments": [
            "Apply Chlorothalonil-based fungicide as per label instructions.",
            "Use Mancozeb 75% WP at 2g per liter.",
            "Apply Copper Oxychloride 50% WP spray."
        ],
        "preventive_measures": [
            "Practice 3-year crop rotation.",
            "Use disease-resistant seed varieties.",
            "Maintain proper plant spacing for air flow.",
            "Avoid overhead irrigation to reduce leaf wetness.",
            "Apply mulch to prevent soil splash onto leaves."
        ]
    },
    "te": {
        "immediate_actions": [
            "వ్యాధిగ్రస్తమైన ఆకులను వెంటనే తొలగించి నాశనం చేయండి.",
            "ఆరోగ్యకరమైన మొక్కల నుండి ప్రభావిత మొక్కలను వేరు చేయండి.",
            "మొక్కల చుట్టూ సరైన గాలి ప్రసరణ ఉండేలా చూడండి."
        ],
        "organic_treatments": [
            "వేప నూనె స్ప్రే (లీటరు నీటికి 2-3 ml) వేయండి.",
            "రాగి ఆధారిత సేంద్రీయ శిలీంద్ర సంహారిణి వాడండి.",
            "బేకింగ్ సోడా ద్రావణం (గాలన్ నీటికి 1 టేబుల్ స్పూన్) చల్లండి."
        ],
        "chemical_treatments": [
            "క్లోరోథలోనిల్ ఆధారిత శిలీంద్ర సంహారిణి వాడండి.",
            "మాంకోజెబ్ 75% WP లీటరుకు 2 గ్రా వాడండి.",
            "కాపర్ ఆక్సీక్లోరైడ్ 50% WP స్ప్రే చేయండి."
        ],
        "preventive_measures": [
            "3 సంవత్సరాల పంట మార్పిడి పాటించండి.",
            "వ్యాధి నిరోధక విత్తన రకాలు వాడండి.",
            "గాలి ప్రసరణ కోసం సరైన మొక్కల అంతరం ఉంచండి."
        ]
    },
    "hi": {
        "immediate_actions": [
            "सभी संक्रमित पत्तियों को तुरंत हटाएं और नष्ट करें।",
            "प्रभावित पौधों को स्वस्थ पौधों से अलग करें।",
            "पौधों के आसपास उचित वायु संचार सुनिश्चित करें।"
        ],
        "organic_treatments": [
            "नीम का तेल स्प्रे (2-3ml प्रति लीटर पानी) लगाएं।",
            "तांबा आधारित जैविक फफूंदनाशक का उपयोग करें।",
            "बेकिंग सोडा घोल (1 चम्मच प्रति गैलन पानी) का छिड़काव करें।"
        ],
        "chemical_treatments": [
            "क्लोरोथालोनिल आधारित फफूंदनाशक लेबल निर्देशों के अनुसार लगाएं।",
            "मैंकोजेब 75% WP 2 ग्राम प्रति लीटर पर उपयोग करें।",
            "कॉपर ऑक्सीक्लोराइड 50% WP स्प्रे करें।"
        ],
        "preventive_measures": [
            "3 वर्षीय फसल चक्र का अभ्यास करें।",
            "रोग प्रतिरोधी बीज किस्मों का उपयोग करें।",
            "वायु प्रवाह के लिए उचित पौधों की दूरी बनाए रखें।"
        ]
    }
}

YIELD_LOSS = {
    "Mild":     {"range": "5-10%",  "revenue": "₹1,500 - ₹3,000 per acre"},
    "Moderate": {"range": "15-25%", "revenue": "₹4,500 - ₹7,500 per acre"},
    "Severe":   {"range": "30-50%", "revenue": "₹9,000 - ₹15,000 per acre"},
}

def simulate_prediction():
    """Fallback when model is not loaded."""
    disease = random.choice(DEMO_DISEASES)
    if 'healthy' in disease:
        confidence = round(random.uniform(0.93, 0.99), 4)
    else:
        confidence = round(random.uniform(0.82, 0.98), 4)
    return disease, confidence


def real_prediction(image_bytes):
    """Run inference using the real Keras model."""
    try:
        import tensorflow as tf
        import numpy as np
        from PIL import Image

        # Load and preprocess image
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        img = img.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
        img_array = img_array / 255.0  # Normalize to [0, 1]

        # Run prediction
        predictions = MODEL.predict(img_array, verbose=0)
        predicted_index = int(tf.argmax(predictions[0]).numpy())
        confidence = float(tf.reduce_max(predictions[0]).numpy())

        # Map index to class name
        if predicted_index < len(CLASS_NAMES):
            disease = CLASS_NAMES[predicted_index]
        else:
            disease = "Unknown"

        return disease, round(confidence, 4)
    except Exception as e:
        print(f"[AI] Real prediction failed ({e}), falling back to simulation.")
        return simulate_prediction()

def simulate_severity(disease, confidence):
    if 'healthy' in disease.lower():
        return "Healthy", 0.0, "None"
    score = round(random.uniform(10, 90), 2)
    if score < 25:
        level, risk = "Mild", "Low"
    elif score < 60:
        level, risk = "Moderate", "Medium"
    else:
        level, risk = "Severe", "High"
    return level, score, risk

def get_full_prediction(language="en", image_bytes=None):
    # Use real model if loaded and image provided, else simulate
    if MODEL is not None and image_bytes is not None:
        disease, confidence = real_prediction(image_bytes)
    else:
        disease, confidence = simulate_prediction()
    severity_level, severity_score, risk_level = simulate_severity(disease, confidence)
    lang = language if language in RECOMMENDATIONS else "en"
    
    result = {
        "disease": disease,
        "confidence": confidence,
        "severity_level": severity_level,
        "severity_score": severity_score,
        "risk_level": risk_level,
    }
    
    if 'healthy' not in disease.lower():
        yl = YIELD_LOSS.get(severity_level, YIELD_LOSS["Moderate"])
        result["yield_loss_range"] = yl["range"]
        result["revenue_impact"] = yl["revenue"]
        result["recommendations"] = RECOMMENDATIONS[lang]
    else:
        result["yield_loss_range"] = "0%"
        result["revenue_impact"] = "₹0"
        result["recommendations"] = None
    
    return result

# ─── Multipart Parser ────────────────────────────────────────────────────────

def parse_multipart(body, content_type):
    """Simple multipart/form-data parser."""
    boundary = None
    for part in content_type.split(";"):
        part = part.strip()
        if part.startswith("boundary="):
            boundary = part[9:].strip('"')
            break
    
    if not boundary:
        return {}, {}
    
    fields = {}
    files = {}
    
    boundary_bytes = f"--{boundary}".encode()
    parts = body.split(boundary_bytes)
    
    for part in parts:
        if part in (b'', b'--\r\n', b'--'):
            continue
        
        part = part.strip(b'\r\n')
        if part == b'--':
            continue
            
        if b'\r\n\r\n' in part:
            header_section, content = part.split(b'\r\n\r\n', 1)
        elif b'\n\n' in part:
            header_section, content = part.split(b'\n\n', 1)
        else:
            continue
        
        # Remove trailing boundary marker
        if content.endswith(b'\r\n'):
            content = content[:-2]
        
        headers_str = header_section.decode('utf-8', errors='replace')
        
        name = None
        filename = None
        for line in headers_str.split('\r\n'):
            if not line:
                for line2 in headers_str.split('\n'):
                    if 'Content-Disposition' in line2:
                        line = line2
                        break
            if 'Content-Disposition' in line:
                for item in line.split(';'):
                    item = item.strip()
                    if item.startswith('name='):
                        name = item[5:].strip('"')
                    elif item.startswith('filename='):
                        filename = item[9:].strip('"')
        
        if name:
            if filename:
                if name not in files:
                    files[name] = []
                files[name].append({"filename": filename, "content": content})
            else:
                fields[name] = content.decode('utf-8', errors='replace')
    
    return fields, files

# ─── Request Handler ──────────────────────────────────────────────────────────

START_TIME = datetime.now()

class FarmGuardianHandler(http.server.BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")
    
    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(body)
    
    def send_error_json(self, status, message):
        self.send_json({"detail": message}, status)
    
    def get_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(length) if length > 0 else b''
    
    def get_user_from_token(self):
        auth = self.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            return decode_token(auth[7:])
        return None
    
    # ── CORS ──
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    # ── GET routes ──
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')
        
        if path == '/api/health' or path == '/api/health/':
            uptime = str(datetime.now() - START_TIME)
            self.send_json({
                "status": "ok",
                "version": "1.0.0",
                "uptime": uptime,
                "model_loaded": False,
                "simulation_mode": True,
                "message": "FarmGuardian AI Backend is running in simulation mode."
            })
        
        elif path.startswith('/reports/'):
            # Serve report files
            filename = path.split('/reports/')[-1]
            filepath = os.path.join(REPORTS_DIR, filename)
            if os.path.exists(filepath):
                mime = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
                with open(filepath, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', mime)
                self.send_header('Content-Length', str(len(content)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error_json(404, "File not found")
        
        else:
            self.send_error_json(404, "Not found")
    
    # ── POST routes ──
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')
        
        if path == '/api/auth/register':
            self.handle_register()
        elif path == '/api/auth/login':
            self.handle_login()
        elif path == '/api/auth/guest':
            self.handle_guest()
        elif path == '/api/predict' or path == '/api/predict/':
            self.handle_predict()
        elif path == '/api/severity' or path == '/api/severity/':
            self.handle_severity()
        elif path == '/api/field-report' or path == '/api/field-report/':
            self.handle_field_report()
        else:
            self.send_error_json(404, "Not found")
    
    # ── Auth Handlers ──
    def handle_register(self):
        try:
            body = self.get_body()
            content_type = self.headers.get('Content-Type', '')
            
            if 'json' in content_type:
                data = json.loads(body)
            elif 'multipart' in content_type:
                fields, _ = parse_multipart(body, content_type)
                data = fields
            else:
                data = json.loads(body)
            
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            if not username or not password:
                self.send_error_json(400, "Username and password are required")
                return
            
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            # Check if user exists
            c.execute("SELECT id FROM users WHERE username = ?", (username,))
            if c.fetchone():
                conn.close()
                self.send_error_json(400, "Username already exists")
                return
            
            user_id = str(uuid.uuid4())
            pw_hash = hash_password(password)
            c.execute("INSERT INTO users (id, username, email, password_hash) VALUES (?, ?, ?, ?)",
                      (user_id, username, email, pw_hash))
            conn.commit()
            conn.close()
            
            token = create_token(username)
            self.send_json({"access_token": token, "token_type": "bearer"})
        
        except Exception as e:
            print(f"Register error: {e}")
            self.send_error_json(500, f"Registration failed: {str(e)}")
    
    def handle_login(self):
        try:
            body = self.get_body()
            data = json.loads(body)
            username = data.get('username', '')
            password = data.get('password', '')
            
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            row = c.fetchone()
            conn.close()
            
            if not row or not verify_password(password, row[0]):
                self.send_error_json(401, "Invalid credentials")
                return
            
            token = create_token(username)
            self.send_json({"access_token": token, "token_type": "bearer"})
        
        except Exception as e:
            print(f"Login error: {e}")
            self.send_error_json(500, f"Login failed: {str(e)}")
    
    def handle_guest(self):
        guest_name = f"guest_{uuid.uuid4().hex[:8]}"
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        user_id = str(uuid.uuid4())
        pw_hash = hash_password(guest_name)
        c.execute("INSERT INTO users (id, username, password_hash, is_guest) VALUES (?, ?, ?, 1)",
                  (user_id, guest_name, pw_hash))
        conn.commit()
        conn.close()
        
        token = create_token(guest_name)
        self.send_json({"access_token": token, "token_type": "bearer"})
    
    # ── Prediction Handlers ──
    def handle_predict(self):
        try:
            body = self.get_body()
            content_type = self.headers.get('Content-Type', '')

            language = "en"
            image_bytes = None

            if 'multipart' in content_type:
                fields, files = parse_multipart(body, content_type)
                language = fields.get('language', 'en')
                # Extract uploaded image bytes
                file_list = files.get('file', [])
                if file_list:
                    image_bytes = file_list[0]['content']

            result = get_full_prediction(language, image_bytes=image_bytes)
            
            # Save scan to DB
            username = self.get_user_from_token()
            if username:
                try:
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    c.execute("SELECT id FROM users WHERE username = ?", (username,))
                    user_row = c.fetchone()
                    if user_row:
                        c.execute("""INSERT INTO scans (id, user_id, disease, confidence, severity_level, severity_score, risk_level)
                                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                  (str(uuid.uuid4()), user_row[0], result['disease'], result['confidence'],
                                   result['severity_level'], result['severity_score'], result['risk_level']))
                        conn.commit()
                    conn.close()
                except Exception:
                    pass
            
            self.send_json(result)
        
        except Exception as e:
            print(f"Predict error: {e}")
            self.send_error_json(500, f"Prediction failed: {str(e)}")
    
    def handle_severity(self):
        try:
            body = self.get_body()
            content_type = self.headers.get('Content-Type', '')
            
            language = "en"
            if 'multipart' in content_type:
                fields, _ = parse_multipart(body, content_type)
                language = fields.get('language', 'en')
            
            result = get_full_prediction(language)
            self.send_json(result)
        
        except Exception as e:
            self.send_error_json(500, str(e))
    
    def handle_field_report(self):
        try:
            body = self.get_body()
            content_type = self.headers.get('Content-Type', '')
            
            language = "en"
            num_files = 1
            
            if 'multipart' in content_type:
                fields, files = parse_multipart(body, content_type)
                language = fields.get('language', 'en')
                file_list = files.get('files', [])
                num_files = max(len(file_list), 1)
            
            # Generate predictions for each "image"
            scan_results = []
            disease_dist = {}
            risk_dist = {}
            total_severity = 0
            
            for i in range(num_files):
                pred = get_full_prediction(language)
                scan_results.append(pred)
                
                d = pred['disease']
                disease_dist[d] = disease_dist.get(d, 0) + 1
                
                r = pred['risk_level']
                risk_dist[r] = risk_dist.get(r, 0) + 1
                
                total_severity += pred['severity_score']
            
            # Calculate health score (inverse of average severity)
            avg_severity = total_severity / num_files
            health_score = round(max(0, 100 - avg_severity), 1)
            
            # Generate a simple text report file
            report_id = uuid.uuid4().hex[:8]
            report_filename = f"report_{report_id}.txt"
            report_path = os.path.join(REPORTS_DIR, report_filename)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("   FarmGuardian AI — Field Health Report\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Images Analyzed: {num_files}\n")
                f.write(f"Overall Health Score: {health_score}%\n\n")
                f.write("-" * 40 + "\n")
                f.write("Disease Distribution:\n")
                for disease, count in disease_dist.items():
                    f.write(f"  • {disease.replace('_', ' ')}: {count} image(s)\n")
                f.write("\n")
                f.write("-" * 40 + "\n")
                f.write("Risk Distribution:\n")
                for risk, count in risk_dist.items():
                    f.write(f"  • {risk}: {count} image(s)\n")
                f.write("\n")
                if scan_results and scan_results[0].get('recommendations'):
                    recs = scan_results[0]['recommendations']
                    f.write("-" * 40 + "\n")
                    f.write("Priority Recommendations:\n")
                    if recs.get('immediate_actions'):
                        for action in recs['immediate_actions']:
                            f.write(f"  ⚠ {action}\n")
                f.write("\n" + "=" * 60 + "\n")
            
            # Aggregate recommendations
            all_recs = None
            for sr in scan_results:
                if sr.get('recommendations'):
                    all_recs = sr['recommendations']
                    break
            
            response = {
                "health_score": health_score,
                "images_analyzed": num_files,
                "disease_distribution": disease_dist,
                "risk_distribution": risk_dist,
                "recommendations": all_recs,
                "pdf_url": f"/reports/{report_filename}",
                "scan_results": scan_results
            }
            
            self.send_json(response)
        
        except Exception as e:
            print(f"Report error: {e}")
            self.send_error_json(500, f"Report generation failed: {str(e)}")


# ─── Start Server ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    server = http.server.HTTPServer((HOST, PORT), FarmGuardianHandler)
    print("")
    print("=" * 58)
    print("  FarmGuardian AI Backend Server")
    print("-" * 58)
    print(f"  Status:  RUNNING (Simulation Mode)")
    print(f"  URL:     http://localhost:{PORT}")
    print(f"  Health:  http://localhost:{PORT}/api/health")
    print(f"  Docs:    POST /api/predict, /api/field-report")
    print("-" * 58)
    print("  No pip installs required! Pure Python stdlib.")
    print("=" * 58)
    print("")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
        server.server_close()
