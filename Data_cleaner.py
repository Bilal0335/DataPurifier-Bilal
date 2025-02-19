import streamlit as st
import pandas as pd
from io import BytesIO
import os

st.set_page_config(page_title="Data Purifier by Bilal", layout="wide")

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .stApp { background-color: #ffff; color: #000000; }
    h1, h2, h3, h4, h5, h6 { color: #00C896; text-align: center; }
    .stButton>button { background-color: #007BFF; color: black; border-radius: 10px; padding: 8px 16px; border: none; }
    .stButton>button:hover { background-color: #0056b3; }
    .stCheckbox label { color: white !important; }
    .dataframe { background-color: #1E1E1E; color: white; border-radius: 10px; padding: 10px; }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("✨Growth Mindset Challenge")
st.write("Welcome to the **Growth Mindset Challenge** Web App!🚀")

# File upload
uploaded_files = st.file_uploader("📂 Upload your CSV or Excel file", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file format ({file_ext}). Please upload a CSV or Excel file.")
            continue

        # Display Data Preview
        st.subheader(f"📊 Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader(f"🧹 Data Cleaning Options for {file.name}")
        if st.checkbox(f"Enable Data Cleaning for {file.name}"):

            col1, col2 = st.columns(2)

            with col1:
                remove_duplicates = st.button(f"🗑️ Remove Duplicates from {file.name}")
                if remove_duplicates:
                    df.drop_duplicates(inplace=True)
                    st.success(f"✅ Duplicate rows removed from {file.name} successfully.")

            with col2:
                handle_missing = st.button(f"🔄 Handle Missing Values in {file.name}")
                if handle_missing:
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success(f"✅ Missing values in {file.name} filled with column mean.")

        # Column Selection
        st.subheader(f"🔍 Select Columns to Keep for {file.name}")
        columns = st.multiselect(
            f"📌 Choose columns to keep from {file.name}", df.columns.tolist(), default=df.columns.tolist()
        )
        df = df[columns]

        # Data Visualization
        st.subheader(f"📈 Data Visualization Options for {file.name}")
        if st.checkbox(f"📊 Enable Data Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Conversion Options
        st.subheader(f"📂 Conversion Options for {file.name}")
        conversion_type = st.radio(f"🛠️ Convert {file.name} to:", ["CSV", "Excel"])

        buffer = BytesIO()
        file_name = file.name.replace(file_ext, ".csv" if conversion_type == "CSV" else ".xlsx")
        mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
        else:
            df.to_excel(buffer, index=False, engine='openpyxl')

        buffer.seek(0)

        # Download Button
        downloaded = st.download_button(
            label=f"📥 Download {file_name}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )

        # ✅ Fixed: Checking if file was downloaded before showing success message
        if downloaded:
            st.success(f"🎉 {file_name} downloaded successfully! 🚀")
