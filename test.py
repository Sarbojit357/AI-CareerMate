import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use a valid model name from your list
model = genai.GenerativeModel("gemini-2.5-flash")

# Generate content
response = model.generate_content("Hello Gemini 2.5! How are you?")
print(response.text)
