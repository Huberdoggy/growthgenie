from persona_loader import load_persona
from trait_modifiers import apply_trait_modifiers


def run_growthgenie():
    print("🤖 GrowthGenie is initializing...")


def generate_prompt(base_prompt, persona_id, external_mode=False, traits_override=None):
    persona = load_persona(persona_id)
    traits = traits_override if traits_override is not None else persona.traits # See related comment in demo_ui
    return apply_trait_modifiers(base_prompt, traits, external_mode)

