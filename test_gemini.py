import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")
if not api_key:
    print("ERROR: No API Key found in environment.")
    exit(1)
genai.configure(api_key=api_key)
print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
print("\nTesting generation with gemini-1.5-flash...")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Explain how AI works in a few words")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error generating content: {e}")