"""
This module applies trait-based transformations to a base prompt.
Each trait acts as a modular filter, layered in order of descending intensity.
"""

# Trait-to-function map for easy extensibility
trait_function_map = {
    "witty": lambda prompt: _add_witty_flair(prompt),
    "curious": lambda prompt: _inject_curiosity(prompt),
    "precise": lambda prompt: _tighten_clarity(prompt),
    # Add more traits later
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
    modified_prompt = base_prompt

    # Sort traits by strength (highest weight first)
    sorted_traits = sorted(traits.items(), key=lambda item: item[1], reverse=True)

    for trait, weight in sorted_traits:
        if weight > 0.7 and trait in trait_function_map:
            modifier_fn = trait_function_map[trait]
            modified_prompt = modifier_fn(modified_prompt) # This actually calls the lambda

    return modified_prompt


# Trait-specific transformation functions
def _add_witty_flair(prompt: str) -> str:
    return f"{prompt}\n\n(But hey — let’s keep it fun. 🤖💡)"


def _inject_curiosity(prompt: str) -> str:
    return f"{prompt}\n\nNow imagine what would happen if we took this even further..."


def _tighten_clarity(prompt: str) -> str:
    return prompt.strip()  # Placeholder: could later run through a simplifier or clarity check
