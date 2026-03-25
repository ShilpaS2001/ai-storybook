import streamlit as st
import PIL.Image
from main_app import generate_full_book
from save_book import create_pdf_buffer

# =========================
# 1. PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Toy Storymaker",
    page_icon="🧸",
    layout="centered"
)

st.title("🧸 AI Toy Storymaker")
st.subheader("Transform your toy into a storybook hero!")

# =========================
# 2. SESSION STATE INIT
# =========================
if "book_data" not in st.session_state:
    st.session_state.book_data = None


# =========================
# 3. SIDEBAR SETTINGS
# =========================
with st.sidebar:
    st.header("Story Settings")

    theme = st.selectbox(
        "Choose a Theme",
        [
            "Space Adventure",
            "Birthday Cake Mountain",
            "Underwater Kingdom",
            "Jungle Explorer"
        ]
    )


# =========================
# 4. IMAGE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "Upload a photo of the toy",
    type=["jpg", "png", "jpeg"]
)


# =========================
# 5. IF IMAGE EXISTS
# =========================
if uploaded_file:

    img = PIL.Image.open(uploaded_file)
    st.image(img, caption="The Main Character", width=300)

    # =========================
    # GENERATE BUTTON
    # =========================
    if st.button("✨ Generate My Storybook"):

        with st.spinner("🔍 Creating your storybook..."):
            st.session_state.book_data = generate_full_book(theme, uploaded_file)

        st.success("✅ Book Ready!")
        st.balloons()


    # =========================
    # DISPLAY BOOK
    # =========================
    if st.session_state.book_data:

        for i, page in enumerate(st.session_state.book_data):

            st.divider()

            # ---------- COVER ----------
            if page.get("type") == "cover":

                st.markdown("## 📘 Book Cover")

                if page.get("image"):
                    st.image(page["image"], use_container_width=True)

                st.markdown(f"### {page.get('title', 'Story Book')}")
                continue

            # ---------- STORY PAGES ----------
            st.markdown(f"### Page {i}")

            if page.get("image"):
                st.image(page["image"], use_container_width=True)

            st.write(page.get("text", ""))


    # =========================
    # PDF DOWNLOAD SECTION
    # =========================
    if st.session_state.book_data:

        st.write("---")
        st.success("Your book is generated! You can download it below.")

        with st.spinner("Finalizing PDF file..."):
            pdf_bytes = create_pdf_buffer(st.session_state.book_data)

        if pdf_bytes:
            st.download_button(
                label="📥 Download your Storybook PDF",
                data=pdf_bytes,
                file_name=f"My_{theme.replace(' ', '_')}_Story.pdf",
                mime="application/pdf",
                key="download_btn"
            )


# =========================
# 6. RESET IF IMAGE REMOVED
# =========================
else:
    st.session_state.book_data = None
    st.info("Please upload a photo of a toy to get started!")