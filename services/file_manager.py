from pathlib import Path
import shutil
import re


BASE_REPORTS_FOLDER = Path("reports")


def sanitize_folder_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-zA-Z0-9_-]+", "-", name)
    return name.strip("-")


def create_report_folder(issue: str) -> Path:
    folder_name = sanitize_folder_name(issue)
    report_folder = BASE_REPORTS_FOLDER / folder_name
    evidences_folder = report_folder / "evidences"

    evidences_folder.mkdir(parents=True, exist_ok=True)

    return report_folder


def save_uploaded_files(uploaded_files, report_folder: Path) -> list[str]:
    evidence_names = []

    if not uploaded_files:
        return evidence_names

    evidences_folder = report_folder / "evidences"

    for uploaded_file in uploaded_files:
        file_path = evidences_folder / uploaded_file.name

        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        # 👇 alteração aqui
        evidence_names.append(f"evidences/{uploaded_file.name}")

    return evidence_names