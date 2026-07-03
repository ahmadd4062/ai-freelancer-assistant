# test_gemini.py
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key found: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit()

try:
    # Initialize client
    client = genai.Client(api_key=api_key)
    
    print("\n=== Trying different models ===\n")
    
    # List of models to try
    models_to_try = [
        "gemini-3.5-flash",
        "gemini-2.5-flash",
        "gemini-pro",
        "gemini-1.0-pro",
        "gemini-2.0-flash",
        "gemini-1.5-flash-001",
        "gemini-1.5-pro-001",
    ]
    
    working_model = None
    
    for model_name in models_to_try:
        try:
            print(f"Testing: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents="Say hello"
            )
            print(f"✅ SUCCESS with {model_name}!")
            print(f"Response: {response.text[:100]}...\n")
            working_model = model_name
            break
        except Exception as e:
            print(f"❌ Failed with {model_name}: {str(e)[:100]}...\n")
    
    if working_model:
        print(f"\n✅ Working model found: {working_model}")
        print(f"Use this in your code: model=\"{working_model}\"")
    else:
        print("\n❌ No working model found. Let's try to list all available models.")
        
        # Try to list all models
        try:
            print("\n=== Available models ===")
            # List models using the client
            # Note: The new client might have different method
            print("Please check https://ai.google.dev/gemini-api/docs/models for available models")
            print("Common models: gemini-1.5-flash, gemini-1.5-pro, gemini-pro")
        except Exception as e:
            print(f"Could not list models: {e}")
            
except Exception as e:
    print(f"ERROR: {e}")