from trait_modifiers import THRESHOLD

def build_trait_explanation(applied_traits: dict) -> str:
  sorted_traits = sorted(applied_traits.items(), key=lambda x: x[1], reverse=True)
  top = [trait for trait, weight in sorted_traits if weight >= THRESHOLD]

  if not top:
      return "No strong personality traits were emphasized in this response."
    
  # Currently, only using the 2 'explanations' for PUBLIC_SAFE_TRAITS
  phrases = {
      "analytical": "I emphasized logic and structured insight",
      "precise": "I clarified language and trimmed ambiguity"
      #"empathetic": "I softened the tone to be more compassionate",
      #"witty": "I added a playful twist",
      #"curious": "I expressed open-ended thinking",
      #"direct": "I delivered with confidence and brevity"
  }

  reasons = [phrases.get(trait, f"I adjusted for {trait}") for trait in top]
  joined = "; ".join(reasons)

  return f"🧠 Why this tone? {joined}."
