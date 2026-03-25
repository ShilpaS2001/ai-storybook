import os
import time
import PIL.Image
from huggingface_hub import InferenceClient
import google.generativeai as genai
import base64
import io
import streamlit as st

# =====================
# 1. API SETUP
# =====================
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
HF_TOKEN = st.secrets["HF_TOKEN"]

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# HuggingFace image model
hf_client = InferenceClient(
    "black-forest-labs/FLUX.1-schnell",
    token=HF_TOKEN
)

print("🔥 RUNNING FILE:", __file__)

# =====================
# 3. MAIN FUNCTION
# =====================
def generate_full_book(theme, uploaded_image=None):
    character_dossier = "Benny the Bear."
    book_results = []

    # =====================
    # PHASE 1: VISION
    # =====================
    if uploaded_image:
        print("🔍 Step 1: Analyzing toy photo...")
        try:
            img = PIL.Image.open(uploaded_image).convert("RGB")
            img.thumbnail((1024, 1024))

            response = model.generate_content([
                "Describe this toy briefly for a children's story. "
                "Include colors, material, and give it a cute name.",
                img
            ])

            character_dossier = response.text
            print("✅ Character Created")

        except Exception as e:
            print(f"❌ VISION ERROR: {e}")

    # =====================
    # PHASE 2: STORY WRITING
    # =====================
    print(f"✍️ Step 2: Writing story about {theme}...")

    prompt = f"""
    You are a professional children's storybook author.

    Write a simple, fun, and heartwarming story for children aged 3 to 7.

    MAIN CHARACTER:
    {character_dossier}

    THEME:
    {theme}

    STORY RULES:
    - Use very simple English
    - Short sentences only
    - 2–3 sentences per page
    - Friendly, happy tone
    - No scary or sad words
    - Give the character a cute name and use it throughout
    - Each page should show a new small event
    - End with a warm and happy ending

    FORMAT EXACTLY LIKE THIS:
    Page 1 Text: ... | Prompt: ...
    Page 2 Text: ... | Prompt: ...
    Page 3 Text: ... | Prompt: ...
    Page 4 Text: ... | Prompt: ...
    """

    try:
        story_response = model.generate_content(prompt)
        story_text = story_response.text

    except Exception as e:
        print(f"❌ STORY ERROR: {e}")
        return []

    # =====================
    # PHASE 3: PARSE & IMAGE GENERATION
    # =====================
    lines = [l.strip() for l in story_text.split("\n") if "|" in l]

    for i, line in enumerate(lines[:4]):
        print(f"🎨 Step 3: Painting page {i+1}...")
        try:
            parts = line.split("|")
            txt = parts[0].split("Text:")[-1].strip()
            prmt = parts[1].split("Prompt:")[-1].strip()

            image = hf_client.text_to_image(
                f"Children's book illustration, watercolor style, soft pastel colors, "
                f"rounded shapes, cute and friendly look. "
                f"Main character: {character_dossier}. Scene: {prmt}"
            )

            img_buffer = io.BytesIO()
            image.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            book_results.append({
                "text": txt,
                "image": img_buffer
            })

        except Exception as e:
            print(f"⚠️ IMAGE ERROR on page {i+1}: {e}")
            book_results.append({
                "text": "The adventure continues...",
                "image": None
            })

    # =====================
    # PHASE 4: COVER GENERATION
    # =====================
    print("🎨 Step 4: Painting the Front Cover...")

    cover_prompt = (
        f"Professional children's book cover illustration, "
        f"title: {theme}, featuring {character_dossier[:60]}"
    )

    try:
        cover_img = hf_client.text_to_image(cover_prompt)

        cover_buffer = io.BytesIO()
        cover_img.save(cover_buffer, format="PNG")
        cover_buffer.seek(0)

        book_results.insert(0, {
            "title": theme,
            "image": cover_buffer,
            "type": "cover"
        })

        print("✅ Front Cover Ready")

    except Exception as e:
        print(f"⚠️ Cover failed: {e}")

    return book_results