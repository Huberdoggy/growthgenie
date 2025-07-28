import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from prompt_logic import generate_prompt
from persona_loader import load_persona
from settings import THRESHOLD, PUBLIC_SAFE_TRAITS

load_dotenv()
# Get the API key from .env
# The OpenAI Python library automatically looks for OPENAI_API_KEY
# but you can explicitly retrieve it if needed for other purposes
openai_api_key = os.getenv("OPENAI_API_KEY")

persona_metadata = {
    "Kyle": {
        "emoji": "🦑",
        "bio": "Sharp-tongued but sincere, Kyle weaves logic with humor. He’s your go-to when clarity meets curiosity."
    },
    "Renae": {
        "emoji": "🧑‍🔬",
        "bio": "Analytical yet warm, Renae sees nuance where others rush."
    }
}


# --- UI Header ---
st.title("🧞 GrowthGenie")
st.caption("Shape the voice of your AI with personality traits. No prompt engineering required.")

# --- Prompt Input ---
user_prompt = st.text_area("💬 Enter your base prompt:", value="Explain how LLMs generate human-like text.")

# --- Persona Selection ---
persona_id = st.selectbox("🎭 Choose a persona:", options=["Kyle", "Renae"])
# --- Persona Preview ---
meta = persona_metadata.get(persona_id)
if meta:
    st.markdown(
        f"""
        <div style="
            background-color: #2a2a2e;
            padding: 10px 16px;
            border-left: 5px solid #007acc;
            border-radius: 8px;
            margin-top: 10px;
            margin-bottom: 10px;
            font-size: 15px;
        ">
        <strong>{meta['emoji']} {persona_id}</strong><br>
        <em>{meta['bio']}</em>
        </div>
        """,
        unsafe_allow_html=True
    )


# --- Trait Slider Preview ---
st.subheader("🎛️ Trait Tuning (0–10)")
all_traits = ["witty", "curious", "empathetic", "analytical", "direct", "imaginative"] # Removed 'precise'

# --- Mode Toggle ---
external_mode = st.checkbox("External Mode (Public-safe output)", value=False)

PRESETS = {
    "Atlas Mode": {"curious": 0.9, "analytical": 0.9, "witty": 0.8},
    "Make It More Human": {"empathetic": 0.9, "witty": 0.8},
    "Brand Voice Booster": {"imaginative": 0.9, "direct": 0.8},
    "The Conversational Researcher": {"curious": 0.8, "empathetic": 0.6, "analytical": 0.5}
}

st.subheader("🧑‍🎓 Guided Mode Presets")

# Filter presets based on mode
if external_mode:
    safe_presets = ["The Conversational Researcher"]
else:
    safe_presets = list(PRESETS.keys())

# Conveniently reset all sliders to zero
if st.button("Reset Traits"):
    st.session_state["selected_preset"] = "None"
    for t in all_traits:
        st.session_state[t] = 0

# 'safe_presets' will either contain only public-mode preset, or all others
selected_preset = st.selectbox(
    "Choose a preset to auto-fill trait sliders:",
    ["None"] + safe_presets,
    key="selected_preset"
)


# Handle preset injection
if selected_preset != "None":
    # First clear all sliders
    for t in all_traits:
        st.session_state[t] = 0

    # Then apply preset values
    for t, v in PRESETS[selected_preset].items():
        st.session_state[t] = int(v * 10)  # scale to 0–10 slider range


trait_inputs = {}
for trait in all_traits:
    if external_mode and trait not in PUBLIC_SAFE_TRAITS:
        continue  # Skip non-public traits when in external mode
    trait_inputs[trait] = st.slider(
        trait.title(), 0, 10, 0, key=trait  # key allows programmatic control via st.session_state
    )
    
# Normalize slider values to 0.0–1.0
normalized_traits = {trait: value / 10 for trait, value in trait_inputs.items()}
nonzero_count = sum(1 for val in normalized_traits.values() if val > 0)

# Control generate button state -> 3 traits for 3 'wishes', so to speak...
generate_disabled = nonzero_count > 3
if generate_disabled:
    st.caption("⚠️ Limit: Please select no more than 3 traits per persona.")

# --- Generate Button ---
if st.button("✨ Generate", disabled=generate_disabled):
    
    # Load persona for reference (could be shown later)
    persona = load_persona(persona_id)

    # Generate tuned prompt. Use persona traits unless user has adjusted sliders
    traits_to_use = normalized_traits if any(normalized_traits.values()) else None

    user_prompt, system_prompt = generate_prompt(
        user_prompt,
        persona_id,
        external_mode=external_mode,
        traits_override=traits_to_use
    )
    
    # --- Output Section ---
    st.markdown("#### 🔮 GrowthGenie Output")
    
    with st.chat_message("assistant"):
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        assistant_reply = response.choices[0].message.content
        
        st.markdown(
            f"""
            <div style="
                background-color: #1c1c1f;
                padding: 12px 16px;
                border-radius: 8px;
                margin-bottom: 6px;
                max-width: 90%;
                word-wrap: break-word;
                color: #ffffff;
                font-style: italic;
                font-size: 1rem;
                border-left: 4px solid #4a4a4d;
            ">
            <strong>💬 You:</strong> {user_prompt}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                background-color: #2a2a2e;
                padding: 16px 18px;
                border-radius: 14px;
                margin-bottom: 16px;
                max-width: 90%;
                word-wrap: break-word;
                box-shadow: 0px 2px 6px rgba(0,0,0,0.3);
                border: 1px solid #3d3d42;
                font-size: 1rem;
                color: #f2f2f2;
            ">
            <strong>Assistant:</strong><br>{assistant_reply}
            </div>
            """,
            unsafe_allow_html=True
        )

        
    # Split prompt from modifiers using double line break
    #base, *modifiers = tuned_prompt.split("\n\n", 1)

    # We've already displayed `base` in the styled bubble.
    # Now just show the rest in the assistant's block.
    # if modifiers:
    #     st.chat_message("assistant").write(modifiers[0])

    if external_mode:
    # Apply same public-safe gating logic for explanation
        filtered_traits = {trait: weight for trait, weight in (traits_to_use or persona.traits).items()
                           if trait in PUBLIC_SAFE_TRAITS and weight >= THRESHOLD}

        if filtered_traits:  # Prevents empty explanation
            st.markdown("---")  # Visual break
            st.caption("🧬 Trait influence breakdown")
            #explanation = build_trait_explanation(filtered_traits)
            #st.markdown(f"<div style='margin-top: 10px; font-style: italic;'>{explanation}</div>", unsafe_allow_html=True)

    
