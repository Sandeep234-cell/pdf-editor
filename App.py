import streamlit as st
import fitz
from io import BytesIO

st.set_page_config(
    page_title="PDF Editor Pro",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF Editor Pro")

menu = st.sidebar.radio(
    "Tools",
    [
        "Upload & Edit",
        "Replace Text",
        "Rotate Pages"
    ]
)

uploaded_pdf = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_pdf:

    pdf_bytes = uploaded_pdf.read()

    if menu == "Replace Text":

        old_text = st.text_input("Find")
        new_text = st.text_input("Replace With")

        if st.button("Replace Text"):

            doc = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

            count = 0

            for page in doc:

                locations = page.search_for(old_text)

                for rect in locations:

                    page.draw_rect(
                        rect,
                        fill=(1, 1, 1)
                    )

                    page.insert_text(
                        (rect.x0, rect.y1 - 2),
                        new_text,
                        fontsize=12
                    )

                    count += 1

            output = BytesIO()

            doc.save(output)

            st.success(
                f"{count} replacements completed"
            )

            st.download_button(
                "Download PDF",
                output.getvalue(),
                "edited.pdf",
                "application/pdf"
            )

    elif menu == "Upload & Edit":

        text = st.text_input(
            "Add New Text"
        )

        if st.button("Insert Text"):

            doc = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

            page = doc[0]

            page.insert_text(
                (100, 100),
                text,
                fontsize=18
            )

            output = BytesIO()

            doc.save(output)

            st.download_button(
                "Download PDF",
                output.getvalue(),
                "edited.pdf",
                "application/pdf"
            )

    elif menu == "Rotate Pages":

        angle = st.selectbox(
            "Rotation",
            [90, 180, 270]
        )

        if st.button("Rotate"):

            doc = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

            for page in doc:
                page.set_rotation(angle)

            output = BytesIO()

            doc.save(output)

            st.download_button(
                "Download PDF",
                output.getvalue(),
                "rotated.pdf",
                "application/pdf"
            )
```
