import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from prompt_logic import generate_prompt
from persona_loader import load_persona
from settings import DRY_MODE, THRESHOLD, PUBLIC_SAFE_TRAITS
from pathlib import Path
from PIL import Image

# -----------------------------------------------------------------------------------
# Resolve Base Paths
base_dir = Path(__file__).parent.parent
static_dir = base_dir / "static"
images_dir = base_dir / "images"

# --- Theme Toggle and CSS Injection ---
mode_toggle = st.toggle("🌙 Dark Mode", value=True, key="toggle_text")
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
st.session_state.theme = "dark" if mode_toggle else "light"
css_file = static_dir / ("dark.css" if st.session_state.theme == "dark" else "light.css")
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

persona_metadata = {
    "Kyle": {"bio": "Sharp-tongued but sincere, Kyle weaves logic with humor."},
    "Renae": {"bio": "Analytical yet warm, Renae sees nuance where others rush."},
}

# -----------------------------------------------------------------------------------
# HEADER
with st.container():
    st.title("GrowthGenie")
    genie_header_path = images_dir / "genie_header.png"
    if genie_header_path.exists():
        genie_img = Image.open(genie_header_path)
        st.image(genie_img, use_container_width=False, width=300)
    st.caption("Shape the voice of your AI with personality traits. No prompt engineering required.")

# --- COLUMNIZED PROMPT + PERSONA SECTION ---
col1, col2 = st.columns([1, 1])
with col1:
    st.text_area("Enter your base prompt:", value="Explain how LLMs generate human-like text.", key="user_prompt")
with col2:
    persona_id = st.selectbox("Choose a persona:", options=["Kyle", "Renae"], key="persona_picker")
    meta = persona_metadata.get(persona_id)
    if meta:
        st.markdown(f"**About this persona:** {meta['bio']}")

# --- PRESETS + EXTERNAL TOGGLE ---
all_traits = ["witty", "curious", "empathetic", "analytical", "direct", "imaginative"]
external_mode = st.checkbox("External Mode (Public-safe output)", value=False, key="external_text")

PRESETS = {
    "Atlas Mode": {"curious": 0.9, "analytical": 0.9, "witty": 0.8},
    "Make It More Human": {"empathetic": 0.9, "witty": 0.8},
    "Brand Voice Booster": {"imaginative": 0.9, "direct": 0.8},
    "The Conversational Researcher": {"curious": 0.8, "empathetic": 0.6, "analytical": 0.5},
}
safe_presets = ["The Conversational Researcher"] if external_mode else list(PRESETS.keys())

st.subheader("Guided Mode Presets")
if st.button("Reset Traits", key="reset_traits"):
    st.session_state["selected_preset"] = "None"
    for t in all_traits:
        st.session_state[t] = 0

selected_preset = st.selectbox("Choose a preset:", ["None"] + safe_presets, key="selected_preset")
if selected_preset != "None":
    for t in all_traits:
        st.session_state[t] = 0
    for t, v in PRESETS[selected_preset].items():
        st.session_state[t] = int(v * 10)

# --- COLUMNIZED SLIDERS ---
with st.container():
    st.subheader("Trait Tuning (0–10)")
    col1, col2, col3 = st.columns(3)
    trait_inputs = {}
    trait_buckets = [[], [], []]
    for i, trait in enumerate(all_traits):
        if external_mode and trait not in PUBLIC_SAFE_TRAITS:
            continue
        trait_buckets[i % 3].append(trait)

    for col, bucket in zip([col1, col2, col3], trait_buckets):
        with col:
            for trait in bucket:
                trait_inputs[trait] = st.slider(trait.title(), 0, 10, 0, key=trait)

# --- NORMALIZE + LIMIT CHECK ---
normalized_traits = {t: v / 10 for t, v in trait_inputs.items()}
generate_disabled = sum(1 for val in normalized_traits.values() if val > 0) > 3
if generate_disabled:
    st.caption("⚠️ Limit: Please select no more than 3 traits per persona.")

# --- GENERATE ---
if st.button("Generate", disabled=generate_disabled, key="generate_button"):
    persona = load_persona(persona_id)
    traits_to_use = normalized_traits if any(normalized_traits.values()) else None
    user_prompt = st.session_state.get("user_prompt", "")
    user_prompt, system_prompt = generate_prompt(user_prompt, persona_id, external_mode=external_mode, traits_override=traits_to_use)

    st.markdown("#### GrowthGenie Output")
    avatar_url = "images/genie_avatar.png"

    with st.chat_message("assistant", avatar=avatar_url):
        if DRY_MODE:
            print("DRY MODE ACTIVE: Simulating response...")
            from trait_modifiers import simulate_response
            assistant_reply = simulate_response(user_prompt, system_prompt)
        else:
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-5-chat-latest",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            assistant_reply = response.choices[0].message.content

        st.markdown(f"**You:** {user_prompt}")
        st.markdown(f"**Assistant:** {assistant_reply}")

        top_traits = {
            trait: weight
            for trait, weight in (traits_to_use or persona.traits).items()
            if weight >= THRESHOLD
        }

        if top_traits:
            names = list(top_traits.keys())
            readable = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
            st.markdown(f"_Reflecting traits: {readable}._")

