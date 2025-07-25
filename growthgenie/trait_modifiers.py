"""
This module applies trait-based transformations to a base prompt.
Each trait acts as a modular filter, layered in order of descending intensity.
"""

# Traits that add a fragment (e.g., witty, empathetic)
trait_fragment_map = {
    "witty": lambda: _add_witty_flair(),
    "curious": lambda: _inject_curiosity(),
    "analytical": lambda: _add_analytical_layer(),
    "empathetic": lambda: _add_empathy_tone(),
    "direct": lambda: _add_direct_summary(),
    "imaginative": lambda: _spark_imagination()
}

# Traits that modify the full prompt directly
trait_modifier_map = {
    "precise": lambda prompt: prompt.strip()
}

def apply_trait_modifiers(base_prompt: str, traits: dict, external_mode: bool) -> str:
    """
    Applies trait-specific modifications to the base prompt.

    Parameters:
        base_prompt (str): The raw prompt to be personality-tuned.
        traits (dict): Dictionary of trait weights, e.g., {"witty": 0.8}
        external_mode (bool): If True, applies safety/style changes for public output.

    Returns:
        str: Modified prompt with layered personality effects.
    """
    prompt = base_prompt

    # Sort traits by strength (highest weight first)
    sorted_traits = sorted(traits.items(), key=lambda item: item[1], reverse=True)
    # Traits that are acceptable for public/external mode
    public_safe_traits = {"analytical", "precise"} 

    for trait, weight in sorted_traits:
        if weight > 0.7:
            if external_mode and trait not in public_safe_traits:
                continue  # Skip all layered behavior for public mode

            # Check for modifier traits
            if trait in trait_modifier_map:
                prompt = trait_modifier_map[trait](prompt) # This actually invokes the lambda

            # Then check for fragment traits
            elif trait in trait_fragment_map:
                prompt += trait_fragment_map[trait]() # No args


    return prompt


# Trait-specific transformation functions
def _add_witty_flair() -> str:
    return "\n\n(But hey — let’s keep it fun. 🤖💡)"


def _inject_curiosity() -> str:
    return "\n\nNow imagine what would happen if we took this even further..."


def _add_analytical_layer() -> str:
    return "\n\n[Breakdown: Step-by-step reasoning follows. 📊🔍]"


def _add_empathy_tone() -> str:
    return "\n\n(And remember — it's okay if this feels overwhelming at first. You're not alone.) 💛"


def _add_direct_summary() -> str:
    return "\n\nTL;DR: Cut to the chase. 🗣️💥"


def _spark_imagination() -> str:
    return "\n\nImagine if this idea were a constellation — what would each star represent?"

