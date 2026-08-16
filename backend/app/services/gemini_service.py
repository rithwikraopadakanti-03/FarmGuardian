import os
import json

try:
    import requests
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def generate_treatment_and_reasoning(disease_name, confidence, weather_info, crop_type="Tomato"):
    """
    Generates structured 5-Day Treatment Plan, Yield Loss, Financial Savings,
    and Weather-aware Spraying Advice using OpenAI API (or Gemini API fallback).
    AI NEVER classifies the disease; it reasons on MobileNetV2's prediction.
    """
    prompt = f"""
    Act as a World-Class Agricultural Scientist & AI Agronomist.
    MobileNetV2 Neural Network classified the crop leaf as: {disease_name} (Confidence: {confidence*100:.1f}%).
    Crop Type: {crop_type}.
    Current Weather: Temperature {weather_info.get('temp_c')}°C, Humidity {weather_info.get('humidity_pct')}%, Rain {weather_info.get('rain_mm')}mm, Wind {weather_info.get('wind_speed_kmh')}km/h.

    Provide a structured JSON response with:
    1. day_1_plan: Immediate action (pruning/isolation)
    2. day_2_plan: Primary organic/chemical spray step
    3. day_3_plan: Inspection & soil/drainage control
    4. day_4_plan: Secondary booster application
    5. day_5_plan: Recovery evaluation & preventive routine
    6. yield_loss_pct: Expected yield loss percentage float (e.g. 25.0)
    7. recovery_prob_pct: Expected recovery probability float (e.g. 88.5)
    8. organic_treatment: Organic spray recipe with dosage
    9. chemical_treatment: Recommended chemical fungicide/pesticide with exact dosage
    10. medicine_cost_inr: Estimated medicine cost in INR
    11. labour_cost_inr: Estimated labour cost in INR
    12. water_cost_inr: Estimated water/fuel cost in INR
    13. expected_savings_inr: Estimated net crop savings value in INR
    14. weather_advice: Contextual recommendation combining disease & weather
    """

    # 1. Try OpenAI API
    if OPENAI_API_KEY and _HAS_REQUESTS:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a world-class AI Agronomist providing JSON output."},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"}
            }
            res = requests.post(url, headers=headers, json=payload, timeout=8)
            if res.status_code == 200:
                text_out = res.json()["choices"][0]["message"]["content"]
                return json.loads(text_out)
        except Exception as e:
            print(f"OpenAI API error: {e}")

    # 2. Try Gemini API
    if GEMINI_API_KEY and _HAS_REQUESTS:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"response_mime_type": "application/json"}
            }
            res = requests.post(url, headers=headers, json=payload, timeout=8)
            if res.status_code == 200:
                text_out = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text_out)
        except Exception as e:
            print(f"Gemini API error: {e}")

    # 3. Domain Agronomy Fallback Generator
    if "healthy" in disease_name.lower():
        return {
            "day_1_plan": "Routine leaf inspection & maintain standard drip irrigation schedule.",
            "day_2_plan": "Foliar application of micronutrient spray (Zinc + Boron 1.5g/L) for lush foliage.",
            "day_3_plan": "Monitor for early pest vectors (whiteflies/aphids) along field margins.",
            "day_4_plan": "Apply organic compost tea or neem oil emulsion (2ml/L) as a natural barrier.",
            "day_5_plan": "Record healthy growth metrics in Farm History log.",
            "yield_loss_pct": 0.0,
            "recovery_prob_pct": 99.0,
            "organic_treatment": "Cold-pressed Neem Oil (2ml/L water) + Panchagavya (3% spray).",
            "chemical_treatment": "None required. Maintain bio-fertilizer schedule.",
            "medicine_cost_inr": 350.0,
            "labour_cost_inr": 400.0,
            "water_cost_inr": 150.0,
            "expected_savings_inr": 28000.0,
            "weather_advice": "Weather is ideal. Continue standard cultural practices and monitor soil moisture."
        }
    elif "early_blight" in disease_name.lower():
        return {
            "day_1_plan": "Prune severely spotted lower leaves displaying target-board lesions & destroy them.",
            "day_2_plan": "Apply Copper Oxychloride 50% WP (2.5g/L) or Chlorothalonil late evening.",
            "day_3_plan": "Ensure drip lines are free of leaks to reduce humidity around foliage.",
            "day_4_plan": "Apply Trichoderma viride bio-fungicide (5g/L) to prevent spore spread.",
            "day_5_plan": "Inspect new leaf flushes for concentric rings & schedule follow-up spray in 10 days.",
            "yield_loss_pct": 28.5,
            "recovery_prob_pct": 86.0,
            "organic_treatment": "Neem seed kernel extract (5%) + Baking soda solution (1 tsp/gallon).",
            "chemical_treatment": "Mancozeb 75% WP @ 2g/L water or Chlorothalonil 75% WP @ 2g/L.",
            "medicine_cost_inr": 850.0,
            "labour_cost_inr": 600.0,
            "water_cost_inr": 250.0,
            "expected_savings_inr": 18500.0,
            "weather_advice": f"Humidity is high ({weather_info.get('humidity_pct', 78)}%). Spray in late evening after 6:00 PM to prevent wash-off."
        }
    else:  # Late blight
        return {
            "day_1_plan": "Immediately isolate affected plant clusters and cut off water-soaked leaves.",
            "day_2_plan": "Apply systemic fungicide Metalaxyl 8% + Mancozeb 64% WP (2g/L water).",
            "day_3_plan": "Clear weeds & improve aeration between rows to accelerate leaf drying.",
            "day_4_plan": "Spray Potassium Phosphite or Copper Hydroxide (2g/L) as a secondary protective shield.",
            "day_5_plan": "Evaluate lesions for grey fungal mold suppression. Re-check in 7 days.",
            "yield_loss_pct": 38.0,
            "recovery_prob_pct": 78.5,
            "organic_treatment": "Copper-based organic fungicide + Compost tea foliar spray.",
            "chemical_treatment": "Cymoxanil + Mancozeb @ 2g/L or Dimethomorph @ 1g/L water.",
            "medicine_cost_inr": 1200.0,
            "labour_cost_inr": 750.0,
            "water_cost_inr": 300.0,
            "expected_savings_inr": 22000.0,
            "weather_advice": "Rain expected within 24 hours. Apply systemic fungicide immediately before rainfall starts."
        }

def ask_farm_advisor(user_question, language="en", context=None):
    """
    Answers farmer questions contextually using OpenAI API (or Gemini API fallback).
    Integrates crop, disease, weather, location, and language (EN, TE, HI).
    """
    lang_name = "Telugu (తెలుగు)" if language == "te" else "Hindi (हिन्दी)" if language == "hi" else "English"
    
    prompt = f"""
    You are FarmGuardian AI Advisor, an expert agronomist assisting an Indian farmer in {lang_name}.
    Context:
    - Recent Disease: {context.get('disease', 'Tomato Early Blight') if context else 'Tomato Early Blight'}
    - Weather: {context.get('weather', '29.5°C, 78% Humidity') if context else '29.5°C'}
    - Farmer Location: Guntur, Andhra Pradesh
    
    Question: "{user_question}"
    
    Respond concisely, clearly, and practical for field application in {lang_name}.
    """

    if OPENAI_API_KEY and _HAS_REQUESTS:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": f"You are an expert AI Agronomist assisting in {lang_name}."},
                    {"role": "user", "content": prompt}
                ]
            }
            res = requests.post(url, headers=headers, json=payload, timeout=6)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenAI advisor error: {e}")

    if GEMINI_API_KEY and _HAS_REQUESTS:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            res = requests.post(url, json=payload, timeout=6)
            if res.status_code == 200:
                return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Gemini advisor error: {e}")

    # Multi-language domain agronomy answer generator for all question types
    q_lower = user_question.lower()
    
    if language == "te":
        if "yellow" in q_lower or "vein" in q_lower or "పసుపు" in q_lower:
            return "ఆకుల ఈనెలు పసుపు రంగులోకి మారడం నైట్రోజన్ లోపం లేదా ముందస్తు తెగులు లక్షణం కావచ్చు. పసుపు ఆకులను తీసివేసి, 19:19:19 ఎరువును స్ప్రే చేయండి."
        elif "fertilizer" in q_lower or "organic" in q_lower or "ఎరువు" in q_lower:
            return "సేంద్రీయ పోషణ కోసం పంచగవ్య (3% స్ప్రే) లేదా వర్మీ కంపోస్ట్‌తో కలిపిన వేప పిండిని (ఎకరాకు 250 కేజీలు) ఉపయోగించడం చాలా మంచిది."
        elif "prevent" in q_lower or "blight" in q_lower or "నివారణ" in q_lower:
            return "తేమ ఉన్న వాతావరణంలో ముందస్తు మచ్చ తెగులును నివారించడానికి క్రమబద్ధమైన నీటి పారుదల మరియు ట్రైకోడెర్మా విరిడే (5గ్రా/లీటర్) స్ప్రే చేయండి."
        elif "spray" in q_lower or "tomorrow" in q_lower or "పిచికారీ" in q_lower:
            return "వాతావరణ తేమ 78% ఉంది. రేపు సాయంత్రం 5:30 నుండి 7:30 మధ్య గాాలి వీచని సమయంలో మంచోజెబ్ (2గ్రా/లీటర్) పిచికారీ చేయడం అత్యుత్తమం."
        return "మీ పంట ఆరోగ్యంగా ఉండటానికి క్రమం తప్పకుండా నీటి పారుదల పరిశీలన మరియు వాతావరణం ఆధారంగా మందులు పిచికారీ చేయడం మంచిది."
        
    elif language == "hi":
        if "yellow" in q_lower or "vein" in q_lower or "पीली" in q_lower:
            return "पत्तियों की शिराओं का पीला पड़ना नाइट्रोजन की कमी या अगेती झुलसा का संकेत है। प्रभावित पत्तियों को हटाएं और N-P-K (19:19:19) का छिड़काव करें।"
        elif "fertilizer" in q_lower or "organic" in q_lower or "उर्वरक" in q_lower:
            return "जैविक पोषण के लिए पंचगव्य (3% स्प्रे) या वर्मीकंपोस्ट के साथ नीम की खली (250 किग्रा/एकड़) का प्रयोग करें।"
        elif "prevent" in q_lower or "blight" in q_lower or "रोकथाम" in q_lower:
            return "नमी वाले मौसम में अगेती झुलसा से बचाव के लिए पत्तियों को सूखा रखें और ट्राइकोडर्मा विरिडे (5 ग्राम/लीटर) का छिड़काव करें।"
        elif "spray" in q_lower or "tomorrow" in q_lower or "छिड़काव" in q_lower:
            return "मौसम में 78% नमी है। कल शाम 5:30 से 7:30 बजे के बीच हवा धीमी होने पर मैंकोजेब (2 ग्राम/लीटर) का छिड़काव करना सर्वोत्तम रहेगा।"
        return "अपनी फसल को स्वस्थ रखने के लिए नियमित सिंचाई और मौसम के अनुसार समय पर छिड़काव करें।"
        
    else:
        if "yellow" in q_lower or "vein" in q_lower:
            return "Yellowing leaf veins indicate Nitrogen deficiency or early fungal infection. Prune yellow lower leaves and apply a balanced N-P-K (19:19:19) foliar spray at 5g/L water."
        elif "fertilizer" in q_lower or "organic" in q_lower:
            return "For organic crop nutrition, apply Panchagavya (3% foliar spray) or Neem cake (250kg/acre) combined with Vermicompost to enrich soil microflora."
        elif "prevent" in q_lower or "blight" in q_lower:
            return "To prevent Early Blight in humid weather, maintain drip irrigation to avoid leaf wetness, prune lower foliage, and spray Trichoderma viride bio-fungicide (5g/L)."
        elif "spray" in q_lower or "tomorrow" in q_lower:
            return "Humidity is currently 78%. Spraying is optimal tomorrow evening between 5:30 PM – 7:30 PM when wind speeds drop below 10 km/h for maximum leaf absorption."
        return "Maintain proper soil drainage, avoid overhead irrigation, and follow the 5-day treatment timeline generated for your crop."
