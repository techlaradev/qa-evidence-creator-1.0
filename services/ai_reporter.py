import streamlit as st
from pathlib import Path
from services.file_manager import create_report_folder, save_uploaded_files
from services.pdf_generator import generate_pdf
from services.ollama_client import ollama_generate
import time

st.set_page_config(page_title="QA Evidence Pack Generator", layout="centered")

st.title("QA Evidence Pack Generator")

# 🎯 tipo de teste
test_type = st.radio(
    "Select test template",
    ["Manual", "API"]
)

issue = st.text_input("Issue / Scenario ID")
scenario_bdd = st.text_area("SCENARIO BDD")
conditions = st.text_area("CONDITIONS")
result = st.text_area("RESULT")
status = st.selectbox("STATUS", ["PASS", "FAIL", "BLOCKED", "NOT EXECUTED"])

# 🧠 toggle IA
use_ai = st.checkbox("🧠 Gerar análise com IA", value=True)
ai_model = "mistral:7b-instruct"

# 📡 dados de API
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

# 📎 upload
uploaded_files = st.file_uploader(
    "Upload evidences",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg", "mp4", "mov", "webm"]
)

# 🚀 gerar report
if st.button("Generate Report"):
    if not issue:
        st.error("Issue / Scenario ID is required.")
    else:
        report_folder = create_report_folder(issue)

        # 💾 salvar evidências
        evidence_names = save_uploaded_files(uploaded_files, report_folder)

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
            "evidences": other_files,
            "image_paths": image_paths,
            "api": api_data,
        }

        # =========================
        # 🧠 IA
        # =========================
        if use_ai and status in ["PASS", "FAIL", "BLOCKED"]:
            with st.spinner("🧠 IA analisando..."):
                ai_text = ollama_generate(prompt=scenario_bdd, model=ai_model)

            data["ai_insight"] = ai_text

            # 💾 salvar no disco
            (report_folder / "ai_insight.txt").write_text(
                ai_text, encoding="utf-8"
            )

            (report_folder / "ai_insight.md").write_text(
                ai_text, encoding="utf-8"
            )
        else:
            data["ai_insight"] = ""

        # =========================
        # 📄 PDF
        # =========================
        pdf_path = generate_pdf(data, report_folder)

        st.success("Report generated successfully!")

        # =========================
        # 🧠 MOSTRAR INSIGHT
        # =========================
        if data.get("ai_insight"):
            st.divider()
            st.subheader("🧠 Insight gerado pela IA")

            # display bonito
            st.markdown(
                f"""
                <div style="
                    background-color:#111;
                    padding:15px;
                    border-radius:10px;
                    border:1px solid #444;
                    color:white;
                ">
                <pre>{data["ai_insight"]}</pre>
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            # ✅ copiar fácil
            with col1:
                st.text_area(
                    "📋 Copiar insight:",
                    value=data["ai_insight"],
                    height=200
                )

            # ✅ download
            with col2:
                st.download_button(
                    label="⬇️ Baixar Insight",
                    data=data["ai_insight"],
                    file_name=f"{issue}_ai_insight.txt",
                    mime="text/plain"
                )
