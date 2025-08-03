import sys

# Constants
DRY_MODE = "--dry" in sys.argv
THRESHOLD = 0.7 # Trait application threshold
# Traits that are acceptable for public/external mode
PUBLIC_SAFE_TRAITS = {"analytical", "curious", "empathetic"}


