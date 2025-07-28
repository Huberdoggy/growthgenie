from settings import PUBLIC_SAFE_TRAITS
from persona_loader import load_persona
from system_prompts_private import get_base_system_prompt

 
def generate_prompt(base_prompt, persona_id, external_mode=False, traits_override=None):
    persona = load_persona(persona_id)
    traits = traits_override if traits_override is not None else persona.traits

    # External mode trait sanitization
    if external_mode:
        traits = {t: v for t, v in traits.items() if t in PUBLIC_SAFE_TRAITS}

    system_prompt = get_base_system_prompt(traits)

    return base_prompt, system_prompt # Tuple, to be unpacked in demo_ui

