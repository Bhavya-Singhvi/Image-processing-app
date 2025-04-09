import streamlit as st
from PIL import Image, ImageEnhance, ImageOps,ImageFilter
import io

st.set_page_config(page_title="Image Editor", layout="wide")

st.title("Image Editing Web App")

uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    
    # Sidebar for feature selection
    st.sidebar.title("Edit Options")

    feature = st.sidebar.radio(
        "Choose a feature to apply",
        ("Resize", "Change Resolution", "Add Filters", "Edge Detection", "Contrast Adjustment", "Rotate/Flip", "Grayscale")
    )

    edited_image = image.copy()

    if feature == "Resize":
        width = st.sidebar.number_input("Width", min_value=10, value=image.width)
        height = st.sidebar.number_input("Height", min_value=10, value=image.height)
        edited_image = edited_image.resize((width, height))

    if feature == "Change Resolution":
        res = st.sidebar.selectbox("Choose Resolution", ["Low", "Medium", "High"])
        quality = {"Low": 20, "Medium": 50, "High": 95}[res]
        buffer = io.BytesIO()
        edited_image.save(buffer, format="JPEG", quality=quality)
        edited_image = Image.open(buffer)

    if feature == "Add Filters":
        filter_type = st.sidebar.selectbox("Filter Type", ["SHARPEN", "SMOOTH", "DETAIL"])
        filters = {
            "SHARPEN": ImageEnhance.Sharpness(edited_image).enhance(2.0),
            "SMOOTH": ImageEnhance.Sharpness(edited_image).enhance(0.5),
            "DETAIL": edited_image.filter(ImageFilter.DETAIL)
        }
        edited_image = filters[filter_type]

    if feature == "Edge Detection":
        edited_image = edited_image.filter(ImageFilter.FIND_EDGES)

    if feature == "Contrast Adjustment":
        contrast_level = st.sidebar.slider("Contrast Level", 0.5, 3.0, 1.0)
        enhancer = ImageEnhance.Contrast(edited_image)
        edited_image = enhancer.enhance(contrast_level)

    if feature == "Rotate/Flip":
        action = st.sidebar.selectbox("Choose Action", ["Rotate 90°", "Rotate 180°", "Rotate 270°", "Flip Horizontal", "Flip Vertical"])
        if "Rotate" in action:
            degree = int(action.split()[1][:-1])
            edited_image = edited_image.rotate(degree, expand=True)
        elif action == "Flip Horizontal":
            edited_image = ImageOps.mirror(edited_image)
        elif action == "Flip Vertical":
            edited_image = ImageOps.flip(edited_image)

    if feature == "Grayscale":
        edited_image = ImageOps.grayscale(edited_image)

    # Before and After Comparison
    st.subheader("Before & After Comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Original Image")
        st.image(image, use_container_width=True)

    with col2:
        st.markdown("### Edited Image")
        st.image(edited_image, use_container_width=True)

    # Download functionality
    img_byte_arr = io.BytesIO()
    edited_image.save(img_byte_arr, format='PNG')
    st.download_button(label="Download Edited Image",
                       data=img_byte_arr.getvalue(),
                       file_name="edited_image.png",
                       mime="image/png")
else:
    st.info("Please upload an image to get started.")
