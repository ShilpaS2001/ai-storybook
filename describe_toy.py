from google import genai
from google.genai import types
import PIL.Image
import time
import streamlit as st

# Before calling the AI again
time.sleep(10) # Wait 5 seconds between calls to stay safe

# Initialize the client
client = genai.Client(st.secrets["GOOGLE_API_KEY"])

def get_character_dossier(my_toy):
    # Load your childhood toy image
    img = PIL.Image.open(my_toy)
    
    prompt = """
    Look at this toy carefully.

    Describe it as a cute character for a children's story.

    Use very simple English.

    Include:
    - What the toy looks like (shape, color, material)
    - A cute name for the toy
    - The toy’s personality (happy, brave, kind, curious)
    - One special or funny feature

    Write in 4–5 short sentences only.
    """


    response = client.models.generate_content(
        model="gemini-flash-latest", # Latest fast multimodal model
        contents=[prompt, img]
    )
    
    return response.text

# Run it!
print("--- CHARACTER DOSSIER ---")
print(get_character_dossier("my_toy.jpg")) # Ensure you have an image named my_toy.jpg in the same folder