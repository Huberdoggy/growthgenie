from settings import USE_API, OPENAI_API_KEY, EXTERNAL_MODE
from prompt_logic import run_growthgenie, generate_prompt

if EXTERNAL_MODE:
    print("🌐 External Mode Active — Safe demo version")
else:
    print("🔧 Internal Mode — Full functionality enabled")
    # Tests...
    run_growthgenie()
    test_persona = generate_prompt("Look at my traits!", "kyle".title(),
                                   EXTERNAL_MODE)
    print(test_persona)

if USE_API and OPENAI_API_KEY:
    print("🔑 API access granted.")
else:
    print("\n🚫 API use disabled. Running in local/dev mode.")
