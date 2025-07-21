import os

# Mode toggles
EXTERNAL_MODE = False  # Manually toggle for internal vs. public demo

USE_API = os.getenv("USE_OPENAI", "false").lower() == "true" #  If .env returns None - will default to False

# Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
