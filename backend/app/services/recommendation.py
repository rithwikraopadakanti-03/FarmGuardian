import json
import os

class RecommendationEngine:
    def __init__(self):
        self.locales = {}
        self.load_locales()

    def load_locales(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        i18n_dir = os.path.join(base_dir, 'i18n')
        
        # Default English fallback
        self.locales['en'] = {
            "Tomato___Early_blight": {
                "immediate_actions": ["Remove infected leaves immediately.", "Avoid overhead watering."],
                "organic_treatments": ["Apply copper-based fungicides.", "Use neem oil spray."],
                "chemical_treatments": ["Apply Chlorothalonil or Mancozeb.", "Use systemic fungicides if severe."],
                "preventive_measures": ["Practice 3-year crop rotation.", "Stake plants for better air circulation."]
            },
            "default": {
                "immediate_actions": ["Isolate affected plants if possible.", "Ensure good drainage."],
                "organic_treatments": ["Apply organic compost tea.", "Use neem oil as a general deterrent."],
                "chemical_treatments": ["Consult local agricultural extension for approved fungicides."],
                "preventive_measures": ["Maintain proper plant spacing.", "Sanitize tools between uses."]
            },
            "healthy": {
                "immediate_actions": ["No immediate action required."],
                "organic_treatments": ["Continue current organic practices."],
                "chemical_treatments": ["None required."],
                "preventive_measures": ["Monitor regularly.", "Maintain proper watering schedule."]
            }
        }

        # Try to load real JSON files if they exist
        for lang in ['en', 'te', 'hi']:
            file_path = os.path.join(i18n_dir, f'{lang}.json')
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'recommendations' in data:
                            self.locales[lang] = data['recommendations']
                except Exception as e:
                    print(f"Error loading {lang}.json: {e}")

    def get_recommendations(self, disease: str, severity: str, language: str = "en"):
        if language not in self.locales:
            language = "en"
            
        dataset = self.locales[language]
        
        if 'healthy' in disease.lower():
            return dataset.get('healthy', self.locales['en']['healthy'])
            
        return dataset.get(disease, dataset.get('default', self.locales['en']['default']))

recommendation_engine = RecommendationEngine()
