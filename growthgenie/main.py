from settings import USE_API, OPENAI_API_KEY, EXTERNAL_MODE
from prompt_logic import run_growthgenie, generate_prompt


if EXTERNAL_MODE:
    print("🌐 External Mode Active — Safe demo version")
    # Tests...
    run_growthgenie()
    renae = generate_prompt("     So basically...GPTs kind of, you know, do this thing where they generate text that feels right?     ", "Renae",
           EXTERNAL_MODE)
    print(renae)
else:
    print("🔧 Internal Mode — Full functionality enabled")
    # Alternative tests...
    run_growthgenie()
    kyle = generate_prompt("Here's my traits!", "Kyle",
                                   EXTERNAL_MODE)
    print(kyle)
    

if USE_API and OPENAI_API_KEY:
    print("🔑 API access granted.")
else:
    print("\n🚫 API use disabled. Running in local/dev mode.")
