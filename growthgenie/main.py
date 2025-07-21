from settings import USE_API, OPENAI_API_KEY, EXTERNAL_MODE
from prompt_logic import run_growthgenie

if EXTERNAL_MODE:
    print("🌐 External Mode Active — Safe demo version")
else:
    print("🔧 Internal Mode — Full functionality enabled")

if USE_API and OPENAI_API_KEY:
    print("🔑 API access granted.")
    run_growthgenie()
else:
    print("🚫 API use disabled. Running in local/dev mode.")

