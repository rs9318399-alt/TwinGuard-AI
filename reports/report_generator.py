from fpdf import FPDF
from datetime import datetime

def generate_report(history, risk_score, recommendation, filename="evil_twin_report.pdf"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_fill_color(30, 30, 46)
    pdf.rect(0, 0, 210, 30, "F")

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_xy(10, 8)
    pdf.cell(0, 12, "Evil Twin Detection Report", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_xy(10, 40)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Risk Score: {risk_score}/100", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(10)
    pdf.multi_cell(0, 8, f"Recommendation: {recommendation}")

    pdf.ln(5)
    pdf.set_x(10)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Session Activity Log:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    for event in history:
        pdf.set_x(10)
        pdf.multi_cell(0, 7, f"{event['timestamp']} - {event['event']}: {event['details']}")

    pdf.output(filename)