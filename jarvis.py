import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

query = input("Enter your query: ")

response = client.models.generate_content(
    model = "gemini-2.0-flash",
    contents = query
)

print(response.text)