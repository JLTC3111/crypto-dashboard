from fpdf import FPDF

def export_pdf(metrics):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Crypto Risk Report", ln=True, align='C')
    pdf.ln(10)
    for key, val in metrics.items():
        pdf.cell(200, 10, txt=f"{key}: {val}", ln=True)
    # Convert bytearray to bytes for Streamlit compatibility
    return bytes(pdf.output(dest='S'))
