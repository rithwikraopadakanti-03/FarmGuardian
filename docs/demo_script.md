# FarmGuardian AI — Live Demo Script

**Time:** 5 Minutes
**Setup Requirements:**
- Backend running on `localhost:8000`
- Frontend running on `localhost:5173`
- Have 2 sample images ready on your desktop (1 diseased tomato leaf, 1 healthy potato leaf)

---

## Minute 0:00 - 1:00 | Introduction & The Problem
**Action:** Show the Pitch Deck (Slides 1-3).
**Speaker:** "Good afternoon judges. Meet FarmGuardian AI. Globally, farmers lose 40% of their crops to diseases because they spot them too late. We've built an AI-powered pocket agronomist that detects diseases early, predicts financial loss, and recommends treatments. Let me show you how it works."

## Minute 1:00 - 1:30 | The Landing Page
**Action:** Switch to the live web app (`localhost:5173`). Slowly scroll through the Home page.
**Speaker:** "This is our platform. We designed it mobile-first because our target users are farmers in the field. It’s clean, fast, and accessible."
**Action:** Click **'Continue as Guest'** (or Login).
**Speaker:** "Farmers don't have time for complex registrations, so we support instant Guest access to get them answers immediately."

## Minute 1:30 - 3:00 | Core Feature: Disease Detection
**Action:** Navigate to the **Disease Detection** tab.
**Speaker:** "Imagine a farmer spots a strange spot on their tomato plant. They snap a picture."
**Action:** Drag and drop the *diseased tomato leaf* image into the upload zone. Click **'Analyze Image'**.
*Pause for 2 seconds while the loading spinner shows.*
**Speaker:** "Our FastAPI backend processes the image, runs it through our MobileNetV2 model, and analyzes the lesion coverage using OpenCV."
**Action:** The results card appears. Point to the different sections.
**Speaker:** "Instantly, we get the result: **Early Blight** with 98% confidence. But we don't stop there. Our Severity Engine calculates that 45% of the leaf is covered, marking it as a 'Moderate' risk. We even translate this into potential yield loss and financial impact, making the threat real."
**Action:** Expand the **'Recommendations'** section.
**Speaker:** "Most importantly, we provide immediate, organic, and chemical treatment advice."

## Minute 3:00 - 4:00 | Field Health Report
**Action:** Navigate to the **Field Report** tab.
**Speaker:** "For larger farms, taking one photo isn't enough. Farmers can upload dozens of photos from across their field."
**Action:** Upload both the diseased and healthy images together. Click **'Generate Report'**.
**Speaker:** "Our system analyzes the batch and generates an overall Field Health Score."
**Action:** Click **'Export as PDF'**. Open the downloaded PDF.
**Speaker:** "It automatically generates a professional, downloadable PDF report that the farmer can share with an agronomist or local cooperative for further assistance."

## Minute 4:00 - 4:45 | Dashboard & Multilingual
**Action:** Navigate to the **Dashboard** tab.
**Speaker:** "All scans feed into an analytics dashboard, helping farmers track disease trends over time."
**Action:** Navigate to **Settings** and change the language to **Telugu** (or Hindi). Go back to the Dashboard.
**Speaker:** "Crucially, technology must be accessible. The entire platform, including AI recommendations, is available in local languages like Telugu and Hindi."

## Minute 4:45 - 5:00 | Closing
**Action:** Switch back to Slide 10 of Pitch Deck.
**Speaker:** "FarmGuardian AI: Early detection, higher yields, empowered farmers. Thank you."

---

## Fallback Plan (If Live Demo Fails)
If the backend crashes or the internet drops:
1. "It seems we have a slight network hiccup. Fortunately, I have a recorded video of the workflow right here."
2. Open the pre-recorded `demo_video.mp4` (make sure you record one before pitching!).
3. Talk over the video using the exact same script above.
