import io
import os
from datetime import datetime
from fpdf import FPDF
from typing import Dict, Any, Optional

class PlantVisionPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(5, 150, 105)
        self.cell(0, 10, "PlantVision AI - Plant Pathology Report", ln=True, align="L")
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 5, "Computer Vision-Powered Crop Disease Diagnosis & Treatment System", ln=True, align="L")
        self.ln(4)
        self.set_draw_color(5, 150, 105)
        self.set_line_width(0.7)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f"PlantVision AI Report | Page {self.page_no()}", align="C")

def _clean_str(text: Any) -> str:
    """Safely encodes strings to latin-1 compatible characters for FPDF."""
    if text is None:
        return ""
    return str(text).encode("latin-1", "replace").decode("latin-1")

def generate_pdf_report(diagnosis_result: Dict[str, Any], image_path: Optional[str] = None) -> bytes:
    pdf = PlantVisionPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Meta Info Section
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(95, 6, f"Target Plant: {_clean_str(diagnosis_result.get('plant_name', 'N/A'))}", ln=False)
    pdf.cell(95, 6, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)

    pdf.cell(95, 6, f"Scientific Name: {_clean_str(diagnosis_result.get('scientific_name', 'N/A'))}", ln=False)
    pdf.cell(95, 6, f"Confidence Score: {_clean_str(diagnosis_result.get('confidence_percent', 'N/A'))}", ln=True)
    pdf.ln(4)

    # Diagnosis Banner Box
    is_healthy = diagnosis_result.get("is_healthy", False)
    severity = diagnosis_result.get("severity", "Moderate")

    if is_healthy:
        pdf.set_fill_color(209, 250, 229)
        pdf.set_text_color(6, 95, 70)
    elif severity == "Severe":
        pdf.set_fill_color(255, 228, 230)
        pdf.set_text_color(159, 18, 57)
    else:
        pdf.set_fill_color(254, 243, 199)
        pdf.set_text_color(146, 64, 14)

    box_y = pdf.get_y()
    pdf.rect(10, box_y, 190, 18, "F")
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Diagnosis: {_clean_str(diagnosis_result.get('predicted_disease', 'N/A'))}", ln=True, align="L")
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, f"Severity: {severity}  |  Pathogen: {_clean_str(diagnosis_result.get('pathogen', 'N/A'))}", ln=True, align="L")
    pdf.ln(6)

    # Image thumbnail if valid
    if image_path and os.path.exists(image_path):
        try:
            current_y = pdf.get_y()
            pdf.image(image_path, x=150, y=current_y, w=40)
        except Exception:
            pass

    # Symptoms
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(5, 150, 105)
    pdf.cell(0, 7, "1. Identified Morphological Symptoms", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)

    symptoms = diagnosis_result.get("symptoms", [])
    for sym in symptoms:
        pdf.multi_cell(0, 6, f"-  {_clean_str(sym)}")
    pdf.ln(3)

    # Treatment Plans
    remedies = diagnosis_result.get("remedies", {})

    # Organic Remedies
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(5, 150, 105)
    pdf.cell(0, 7, "2. Recommended Organic Solutions", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    for org in remedies.get("organic", []):
        pdf.multi_cell(0, 6, f"-  {_clean_str(org)}")
    pdf.ln(3)

    # Chemical Treatments
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(5, 150, 105)
    pdf.cell(0, 7, "3. Recommended Chemical Fungicides", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    for chem in remedies.get("chemical", []):
        pdf.multi_cell(0, 6, f"-  {_clean_str(chem)}")
    pdf.ln(3)

    # Preventative Measures
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(5, 150, 105)
    pdf.cell(0, 7, "4. Preventative Best Practices", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    for prev in remedies.get("prevention", []):
        pdf.multi_cell(0, 6, f"-  {_clean_str(prev)}")

    out = pdf.output()
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    return str(out).encode("latin-1")


