import streamlit as st
from prompt_logic import generate_prompt
from persona_loader import load_persona

# --- UI Header ---
st.title("🧞 GrowthGenie")
st.caption("Shape the voice of your AI with personality traits. No prompt engineering required.")

# --- Prompt Input ---
user_prompt = st.text_area("💬 Enter your base prompt:", value="Explain how LLMs generate human-like text.")

# --- Persona Selection ---
persona_id = st.selectbox("🎭 Choose a persona:", options=["kyle", "renae"])

# --- Trait Slider Preview ---
st.subheader("🎛️ Trait Tuning (0–10)")
trait_inputs = {
    "witty": st.slider("Witty", 0, 10, 0),
    "curious": st.slider("Curious", 0, 10, 0),
    "precise": st.slider("Precise", 0, 10, 0),
    "empathetic": st.slider("Empathetic", 0, 10, 0),
    "analytical": st.slider("Analytical", 0, 10, 0),
    "direct": st.slider("Direct", 0, 10, 0),
    "imaginative": st.slider("Imaginative", 0, 10, 0),
}

# --- Mode Toggle ---
external_mode = st.checkbox("External Mode (Public-safe output)", value=False)

# --- Generate Button ---
if st.button("✨ Generate"):
    # Normalize slider values to 0.0–1.0
    normalized_traits = {trait: value / 10 for trait, value in trait_inputs.items()}

    # Load persona for reference (could be shown later)
    persona = load_persona(persona_id)

    # Generate tuned prompt. Use persona traits unless user has adjusted sliders
    traits_to_use = normalized_traits if any(normalized_traits.values()) else None

    tuned_prompt = generate_prompt(
        user_prompt,
        persona_id,
        external_mode=external_mode,
        traits_override=traits_to_use
    )

    st.markdown("#### 🔮 GrowthGenie Output")
    st.markdown(tuned_prompt)
