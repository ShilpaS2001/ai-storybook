import os
from huggingface_hub import InferenceClient
from PIL import Image
import streamlit as st

# 1. Setup your Free Hugging Face Token
# Get one at: https://huggingface.co/settings/tokens
HF_TOKEN = st.secrets["HF_TOKEN"]

# Initialize the client with a high-quality model
# 'FLUX.1-schnell' is one of the best free-to-use models in late 2025
client = InferenceClient("black-forest-labs/FLUX.1-schnell", token=HF_TOKEN)

def generate_storybook_image(prompt, filename="test_page.png"):
    print(f"🎨 Generating: {prompt}...")
    
    try:
        # Use the Hugging Face Inference API
        # This returns a PIL.Image object
        image = client.text_to_image(
            prompt=f"Children's book illustration, vibrant colors, Pixar style, {prompt}",
            width=1024,
            height=768
        )
        
        # Save to your computer
        image.save(filename)
        print(f"✨ Success! Image saved as: {filename}")
        
        # Open the image automatically to show you the result
        image.show()
        
    except Exception as e:
        print(f"❌ Error: {e}")

# --- TEST IT ---
test_prompt = "A green rubber duck and a yellow rubber duck sitting on a giant chocolate birthday cake."
generate_storybook_image(test_prompt)