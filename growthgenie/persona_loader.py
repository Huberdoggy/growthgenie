import json
import os

# Structured persona object
class Persona:
    def __init__(self, name, age, profession, traits):
        self.name = name
        self.age = age
        self.profession = profession
        self.traits = traits

def load_persona(persona_id: str) -> Persona:
    # The below ensures we always use the script's directory as base (Replit might adjust CWD)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, "personas", f"{persona_id.lower()}.json")

    #print(f"Loading persona from: {filepath}")  # Debug check...

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No persona found for ID: {persona_id}")

    with open(filepath, "r") as file:
        data = json.load(file)

    return Persona(
        name=data["name"],
        age=data.get("age"),
        profession=data.get("profession"),
        traits=data["traits"]
    )


