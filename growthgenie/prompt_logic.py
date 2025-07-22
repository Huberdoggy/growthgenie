from persona_loader import load_persona
from trait_modifiers import apply_trait_modifiers


def run_growthgenie():
    print("🤖 GrowthGenie is initializing...")


# Begin prompt logic and persona config (Phase 2+)


def generate_prompt(base_prompt: str,
                    persona_id: str,
                    external_mode: bool = False) -> str:
    persona = load_persona(persona_id)
    tuned_prompt = apply_trait_modifiers(base_prompt, persona["traits"],
                                         external_mode)
    return tuned_prompt
