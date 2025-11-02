# GrowthGenie

GrowthGenie is a personality-powered prompt calibration tool designed for AI solutions strategists.

🛑 **This project is no longer being actively maintained.**
> 📌 *The following documentation remains in place for referential purposes only.*

## Getting Started

1. Clone repo or open in Replit
2. Install dependencies:
   - If you're in the **repo root**, run:
     ```bash
     pip install -r requirements.txt
     ```
   - If you're inside the nested `/growthgenie` folder, run:
     ```bash
     pip install -r ../requirements.txt
     ```
3. Copy `.env.example` to `.env` and populate your OpenAI key
4. To launch the web interface, run:
   ```bash
   streamlit run demo_ui.py
*OPTIONAL:* Include argument *--dry* for simulating responses  
*(If using Replit, click the green Run button.)*

This is a layered build. See commit notes or comments for each phase.

> 🔐 Curious how the model actually interprets trait sliders?
> That magic lives behind the curtain for now — but the interface is yours to remix.
