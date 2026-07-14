class YieldPredictor:
    def __init__(self):
        # Format: (min_loss_multiplier, max_loss_multiplier, base_revenue_per_acre_in_INR)
        self.YIELD_LOSS_TABLE = {
            'Tomato___Early_blight': (0.15, 0.30, 150000),
            'Tomato___Late_blight': (0.30, 0.70, 150000),
            'Potato___Early_blight': (0.10, 0.30, 120000),
            'Potato___Late_blight': (0.40, 0.80, 120000),
            'Corn_(maize)___Common_rust_': (0.10, 0.25, 80000),
            # Default for others
            'default': (0.10, 0.35, 100000)
        }

    def predict_yield_loss(self, disease: str, severity_score: float):
        if 'healthy' in disease.lower():
            return "0%", "₹0"

        params = self.YIELD_LOSS_TABLE.get(disease, self.YIELD_LOSS_TABLE['default'])
        min_mult, max_mult, revenue = params
        
        # Scale by severity score (0 to 100)
        scale = severity_score / 100.0
        
        min_loss = int((min_mult * scale) * 100)
        max_loss = int((max_mult * scale) * 100)
        
        # Ensure minimums for realistic ranges
        min_loss = max(1, min_loss)
        max_loss = max(min_loss + 5, max_loss)
        
        min_revenue_loss = int(revenue * (min_loss / 100.0))
        max_revenue_loss = int(revenue * (max_loss / 100.0))
        
        yield_loss_range = f"{min_loss}-{max_loss}%"
        revenue_impact = f"₹{min_revenue_loss:,} - ₹{max_revenue_loss:,} per acre"
        
        return yield_loss_range, revenue_impact

yield_predictor = YieldPredictor()
