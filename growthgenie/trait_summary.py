# from settings import THRESHOLD

"""
THIS MODULE IS NOT USED IN THE CURRENT VERSION OF THE APP
Kept for reference and potential future use.

This module builds an explanatory string, describing
how a given trait was applied to a base prompt transformation;
if chosen slider intensity met or exceeded the 'threshold' in play.
"""

# def build_trait_explanation(applied_traits: dict) -> str:
#   sorted_traits = sorted(applied_traits.items(), key=lambda x: x[1], reverse=True)
#   top = [trait for trait, weight in sorted_traits if weight >= THRESHOLD]

#   if not top:
#       return "No strong personality traits were emphasized in this response."
    
#   phrases = {
#       "analytical": "I emphasized logic and structured insight",
#       "empathetic": "I softened the tone to be more compassionate",
#       "curious": "I expressed open-ended thinking",
#       "precise": "I clarified language and trimmed ambiguity",
#       "witty": "I added a playful twist",
#       "direct": "I delivered with confidence and brevity"
#   }

#   reasons = [phrases.get(trait, f"I adjusted for {trait}") for trait in top]
#   joined = "; ".join(reasons)

#   return f"🧠 Why this tone? {joined}."
