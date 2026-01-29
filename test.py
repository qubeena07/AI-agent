import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Key missing from .env")
    exit()

print("🔍 Scanning your API key for available models...")

# We use the 'list models' endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS! Here are the models you can use:")
        print("-" * 40)
        found_any = False
        for model in data.get('models', []):
            if 'generateContent' in model.get('supportedGenerationMethods', []):
                print(f"• {model['name']}") # This prints the EXACT name to use
                found_any = True
        
        if not found_any:
            print("⚠️ No content generation models found. Your API is enabled but has no model access.")
    else:
        print(f"\n❌ FAILED to list models. Status: {response.status_code}")
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Error: {e}")