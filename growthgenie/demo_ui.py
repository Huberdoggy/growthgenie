import streamlit as st
from prompt_logic import generate_prompt
from persona_loader import load_persona
from explanation_builder import build_trait_explanation
from trait_modifiers import THRESHOLD, PUBLIC_SAFE_TRAITS

# --- UI Header ---
st.title("🧞 GrowthGenie")
st.caption("Shape the voice of your AI with personality traits. No prompt engineering required.")

# --- Prompt Input ---
user_prompt = st.text_area("💬 Enter your base prompt:", value="Explain how LLMs generate human-like text.")

# --- Persona Selection ---
persona_id = st.selectbox("🎭 Choose a persona:", options=["Kyle", "Renae"])

# --- Trait Slider Preview ---
st.subheader("🎛️ Trait Tuning (0–10)")
all_traits = ["witty", "curious", "precise", "empathetic", "analytical", "direct", "imaginative"]

# --- Mode Toggle ---
external_mode = st.checkbox("External Mode (Public-safe output)", value=False)

trait_inputs = {}
for trait in all_traits:
    if external_mode and trait not in PUBLIC_SAFE_TRAITS:
        continue  # Skip non-public traits when in external mode
    trait_inputs[trait] = st.slider(trait.title(), 0, 10, 0)

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

    # --- Output Section ---
    st.markdown("#### 🔮 GrowthGenie Output")
    st.caption("Here’s how your tuned AI responded:")
    st.markdown(
        f"""
        <div style="
            background-color: black;
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 10px;
            max-width: 90%;
            word-wrap: break-word;
        ">
            <strong>💬 You asked:</strong><br><em>{user_prompt}</em>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Split prompt from modifiers using double line break
    base, *modifiers = tuned_prompt.split("\n\n", 1)

    # We've already displayed `base` in the styled bubble.
    # Now just show the rest in the assistant's block.
    if modifiers:
        st.chat_message("assistant").write(modifiers[0])

    if external_mode:
    # Apply same public-safe gating logic for explanation
        filtered_traits = {trait: weight for trait, weight in (traits_to_use or persona.traits).items()
                           if trait in PUBLIC_SAFE_TRAITS and weight >= THRESHOLD}

        if filtered_traits:  # Prevents empty explanation
            st.markdown("---")  # Visual break
            st.caption("🧬 Trait influence breakdown")
            explanation = build_trait_explanation(filtered_traits)
            st.markdown(f"<div style='margin-top: 10px; font-style: italic;'>{explanation}</div>", unsafe_allow_html=True)

    
