import streamlit as st
from pathlib import Path
from services.file_manager import create_report_folder, save_uploaded_files
from services.pdf_generator import generate_pdf

st.set_page_config(page_title="QA Evidence Pack Generator", layout="centered")

st.title("QA Evidence Pack Generator")

test_type = st.radio(
    "Select test template",
    ["Manual", "API"]
)

issue = st.text_input("Issue / Scenario ID")
scenario_bdd = st.text_area("SCENARIO BDD")
conditions = st.text_area("CONDITIONS")
result = st.text_area("RESULT")
status = st.selectbox("STATUS", ["PASS", "FAIL", "BLOCKED", "NOT EXECUTED"])

api_data = {}

if test_type == "API":
    st.subheader("API Details")

    api_data["method"] = st.selectbox(
        "Method",
        ["GET", "POST", "PUT", "PATCH", "DELETE"]
    )

    api_data["endpoint"] = st.text_input("Endpoint")
    api_data["curl"] = st.text_area("cURL")
    api_data["response"] = st.text_area("Response")

uploaded_files = st.file_uploader(
    "Upload evidences",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg", "mp4", "mov", "webm"]
)

if st.button("Generate Report"):
    if not issue:
        st.error("Issue / Scenario ID is required.")
    else:
        report_folder = create_report_folder(issue)

        # salva arquivos
        evidence_names = save_uploaded_files(uploaded_files, report_folder)

        # 👇 NOVO: separar imagens
        image_paths = []
        other_files = []

        for file_name in evidence_names:
            file_path = report_folder / file_name

            if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                image_paths.append(file_path)
            else:
                other_files.append(file_name)

        data = {
            "test_type": test_type,
            "issue": issue,
            "scenario_bdd": scenario_bdd,
            "conditions": conditions,
            "result": result,
            "status": status,
            "evidences": other_files,  # 👈 vídeos e outros
            "image_paths": image_paths,  # 👈 IMAGENS PRO PDF
            "api": api_data,
        }

        pdf_path = generate_pdf(data, report_folder)

        st.success("Report generated successfully!")
        st.write(f"Folder: `{report_folder}`")
        st.write(f"PDF: `{pdf_path}`")