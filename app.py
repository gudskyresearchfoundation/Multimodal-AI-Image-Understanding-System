import streamlit as st
from PIL import Image
import tempfile
import os
import time

from vlm_engine import describe_image_with_qwen

# --- Page config (must be first Streamlit command) ---
st.set_page_config(page_title="Multimodal AI App", layout="wide")

# --- Default credentials ---
DEFAULT_EMAIL = "user@example.com"
DEFAULT_PASSWORD = "password123"

# --- Session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page():
    st.title("Multimodal AI Image Understanding System")
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email == DEFAULT_EMAIL and password == DEFAULT_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown("---")
    st.info("Use the following credentials:")
    st.code(f"Email: {DEFAULT_EMAIL}\nPassword: {DEFAULT_PASSWORD}")


# --- Check login ---
if not st.session_state.logged_in:
    login_page()
    st.stop()


# --- Main App ---
st.title("Multimodal AI Image Understanding System")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "webp"]
)

question = st.text_input("Ask a question about the image", value="Describe this image clearly.")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Analyze Image"):
        start_total = time.time()
        image_path = None

        try:
            # Save uploaded image to a temporary file
            start_save = time.time()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                image.save(tmp.name)
                image_path = tmp.name
            save_time = time.time() - start_save

            # Run VLM inference
            with st.spinner("Analyzing image with Qwen2.5-VL..."):
                start_infer = time.time()
                response = describe_image_with_qwen(image_path, question)
                infer_time = time.time() - start_infer

            total_time = time.time() - start_total

            # Output
            st.subheader("Model Response")
            st.write(response)

            # Timing info
            st.markdown("---")
            st.write(f"**Image save time:** {save_time:.2f} seconds")
            st.write(f"**Backend inference time:** {infer_time:.2f} seconds")
            st.write(f"**Total app time:** {total_time:.2f} seconds")

        except Exception as e:
            st.error(f"Error: {e}")

        finally:
            if image_path and os.path.exists(image_path):
                os.remove(image_path)