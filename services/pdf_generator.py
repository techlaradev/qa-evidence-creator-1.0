from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def draw_section(pdf, title: str, content: str, y: int) -> int:
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, title)
    y -= 20

    pdf.setFont("Helvetica", 10)

    if not content:
        content = "-"

    for line in content.split("\n"):
        pdf.drawString(60, y, line[:100])
        y -= 15

        if y < 80:
            pdf.showPage()
            y = 800

    y -= 15
    return y


def draw_images(pdf, image_paths: list, y: int) -> int:
    for image_path in image_paths:
        try:
            pdf.drawImage(str(image_path), 60, y - 200, width=400, height=200)
            y -= 220

            if y < 80:
                pdf.showPage()
                y = 800

        except Exception:
            pdf.drawString(60, y, f"Erro ao carregar imagem: {image_path}")
            y -= 20

    return y


def generate_pdf(data: dict, report_folder: Path) -> Path:
    pdf_path = report_folder / "report.pdf"

    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)

    y = 800

    # 🧾 HEADER
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "QA Evidence Report")
    y -= 30

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Issue: {data['issue']}")
    y -= 20

    pdf.drawString(50, y, f"Template: {data['test_type']}")
    y -= 30

    # 📄 SEÇÕES
    y = draw_section(pdf, "SCENARIO BDD", data["scenario_bdd"], y)
    y = draw_section(pdf, "CONDITIONS", data["conditions"], y)

    if data["test_type"] == "API":
        api = data["api"]
        y = draw_section(pdf, "REQUEST / CURL", api.get("curl", ""), y)
        y = draw_section(pdf, "RESPONSE", api.get("response", ""), y)

    evidences = "\n".join(data["evidences"]) if data["evidences"] else "-"
    y = draw_section(pdf, "EVIDENCES", evidences, y)

    # 🖼️ IMAGENS (AQUI É O DIFERENCIAL)
    if data.get("image_paths"):
        y = draw_images(pdf, data["image_paths"], y)

    # 📊 RESULTADO FINAL
    y = draw_section(pdf, "RESULT", data["result"], y)
    y = draw_section(pdf, "STATUS", data["status"], y)

    pdf.save()

    return pdf_path