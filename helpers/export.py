from fpdf import FPDF
import io
from typing import Dict, Any, Optional

def export_pdf(metrics: Dict[str, Any]) -> Optional[bytes]:
    """
    Generate a PDF report with the provided metrics
    
    Args:
        metrics: Dictionary containing report metrics
    
    Returns:
        bytes: PDF file content as bytes, or None if error
    """
    try:
        if not metrics:
            metrics = {"Status": "No data available"}
        
        # Create PDF instance
        pdf = FPDF()
        pdf.add_page()
        
        # Add title
        pdf.set_font("Arial", size=16, style='B')
        pdf.cell(200, 10, txt="Crypto Risk Report", ln=True, align='C')
        pdf.ln(10)
        
        # Add timestamp
        from datetime import datetime
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 8, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        pdf.ln(5)
        
        # Add metrics
        pdf.set_font("Arial", size=12)
        for key, val in metrics.items():
            # Ensure values are string type
            key_str = str(key)
            val_str = str(val) if val is not None else "N/A"
            
            # Truncate long values to prevent PDF issues
            if len(val_str) > 100:
                val_str = val_str[:97] + "..."
            
            pdf.cell(200, 10, txt=f"{key_str}: {val_str}", ln=True)
        
        # Convert bytearray to bytes for Streamlit compatibility
        return bytes(pdf.output(dest='S'))
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        # Return a minimal error PDF
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Error generating report", ln=True, align='C')
            pdf.cell(200, 10, txt=f"Error: {str(e)[:50]}", ln=True, align='C')
            return bytes(pdf.output(dest='S'))
        except:
            return None
