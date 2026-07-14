# FarmGuardian AI - Hackathon Presentation Content

## Elevator Pitch (60 Seconds)
"Globally, farmers lose up to 40% of their crops to diseases, often because they identify the problem too late. This leads to massive financial losses and overuse of chemical pesticides. Meet **FarmGuardian AI** — an early crop disease detection system. By simply taking a photo of a leaf on their smartphone, our AI instantly identifies the disease, assesses its severity, predicts potential yield loss, and provides actionable, multilingual treatment advice. We're turning reactive farming into proactive crop management, saving yields, reducing chemical use, and protecting farmer livelihoods."

## Pitch Deck Outline (10 Slides)

### Slide 1: Title
*   **Headline:** FarmGuardian AI
*   **Sub-headline:** Early Crop Disease Detection & Yield Loss Prevention
*   **Visual:** High-quality image of a healthy crop next to a farmer using a smartphone.

### Slide 2: The Problem
*   **Key Stat:** Up to 40% of global crop yields are lost to pests and diseases (FAO).
*   **Pain Point:** Late detection leads to catastrophic yield loss and reactive, excessive pesticide use.
*   **Impact:** Severe financial instability for rural farmers.

### Slide 3: Our Solution
*   **Concept:** An AI-powered pocket agronomist.
*   **Core Functions:** Detect disease → Assess Severity → Predict Financial Impact → Recommend Treatment.
*   **Key Advantage:** Early intervention prevents spread and minimizes damage.

### Slide 4: How It Works
*   **Visual:** Simple 3-step diagram (Upload Photo → AI Analysis → Results & Action Plan).
*   **Tech Mention:** Powered by MobileNetV2 Transfer Learning and FastAPI.

### Slide 5: Key Features (The "Wow" Factor)
*   **Multilingual:** Accessible in English, Telugu, and Hindi.
*   **Severity Engine:** Doesn't just say *what* it is, but *how bad* it is using computer vision (lesion coverage).
*   **Field Health Reports:** Batch processing with automated PDF generation for entire fields.

### Slide 6: Live Demo Placeholder
*   *(Switch to live application)*

### Slide 7: Technology Stack
*   **Frontend:** React, Vite, Tailwind CSS (Glassmorphism design).
*   **Backend:** FastAPI, Python, SQLite.
*   **AI/ML:** TensorFlow, OpenCV, MobileNetV2 trained on PlantVillage (38 classes).

### Slide 8: Business Impact & Sustainability
*   **Economic:** Increases farmer revenue by preventing 15-30% yield losses.
*   **Environmental (Green Tech):** Promotes targeted, organic treatments first, reducing overall chemical pesticide runoff.

### Slide 9: Future Roadmap
*   **Phase 2:** Integration with local weather APIs for predictive outbreak warnings.
*   **Phase 3:** Drone imagery integration for large-scale farm scanning.
*   **Phase 4:** Community marketplace for farmers to buy recommended treatments directly.

### Slide 10: Team & Conclusion
*   "Protecting crops. Empowering farmers."
*   Team members & roles.
*   Call to Action (e.g., "Try the demo today!").

---

## Anticipated Q&A

**Q: How accurate is the model?**
**A:** Our MobileNetV2 model achieves ~95%+ accuracy on the PlantVillage validation set. We use data augmentation to improve robustness against varying lighting and angles found in the field.

**Q: Does this work offline?**
**A:** The current MVP requires an internet connection to access the FastAPI backend. However, our architecture uses TFLite, meaning the model can easily be deployed entirely on-device (edge AI) in future versions for completely offline use.

**Q: How do you handle crops or diseases not in your dataset?**
**A:** The model outputs a confidence score. If the score is below a certain threshold (e.g., 60%), the system flags it as "Unknown/Requires Expert Review" rather than giving a false positive.
