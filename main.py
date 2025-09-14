# Save as: ppi_streamlit.py
# Run with: streamlit run ppi_streamlit.py

import streamlit as st
from fpdf import FPDF
import datetime
import os

# ---------------------- Configuration ----------------------
SHOP_NAME = "AUTO MAZEN"
SHOP_ADDRESS = "Precision. Performance. Detailing."
SHOP_PHONE = ""
LOGO_PATH = "logo.jpeg"  # optional
REPORTS_DIR = "reports"

if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

CHECK_ITEMS = [
    "Engine - Visual & Oil Leaks",
    "Engine - Compression / Idle / Noises",
    "Transmission / Clutch",
    "Brakes - Pads / Rotors / Fluid",
    "Suspension & Steering",
    "Tires - Tread & Pressure",
    "Exhaust System",
    "Cooling System - Radiator / Hoses",
    "Battery & Charging System",
    "Lights & Electrical",
    "Air Conditioning / Heating",
    "Interior - Seats / Electronics",
    "Body - Rust / Paint / Panels",
    "Frame & Underbody",
    "Test Drive - Noise / Vibration / Handling",
]

RECOMMENDATIONS = [
    "Buy as-is",
    "Negotiate price (minor issues)",
    "Get major repairs before buying",
    "Avoid purchase - too risky",
]

# ---------------------- PDF Helper ----------------------
class InspectionPDF(FPDF):
    def header(self):
        if LOGO_PATH and os.path.exists(LOGO_PATH):
            try:
                self.image(LOGO_PATH, 10, 8, 30)
            except Exception:
                pass
        self.set_font('Arial', 'B', 14)
        self.cell(0, 6, SHOP_NAME, ln=True, align='R')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, SHOP_ADDRESS + (' | ' + SHOP_PHONE if SHOP_PHONE else ''), ln=True, align='R')
        self.ln(4)

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, f'Report generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True, align='L')
        self.cell(0, 5, 'Thank you for choosing ' + SHOP_NAME, ln=True, align='R')


# ---------------------- Streamlit App ----------------------
st.title("Pre-Purchase Vehicle Inspection (PPI)")

# Client & Vehicle Details
with st.expander("Client Details", expanded=True):
    client_name = st.text_input("Client Name")
    client_phone = st.text_input("Phone")
    inspector = st.text_input("Inspector")

with st.expander("Vehicle Details", expanded=True):
    vehicle_model = st.text_input("Make / Model")
    vehicle_year = st.text_input("Year")
    vehicle_vin = st.text_input("VIN / Reg")

# Inspection Checklist
st.subheader("Inspection Checklist")

check_data = []
for item in CHECK_ITEMS:
    cols = st.columns([3, 1, 4, 1])
    status = cols[1].selectbox(f"{item}", ["Pass", "Minor", "Major"], key=f"status_{item}")
    notes = cols[2].text_input("Notes", key=f"notes_{item}")
    cost = cols[3].number_input("Est Cost", min_value=0.0, key=f"cost_{item}", format="%.2f")
    check_data.append((item, status, notes, cost))

# Summary & Recommendation
summary = st.text_area("Summary / Notes")
recommendation = st.selectbox("Recommendation", RECOMMENDATIONS)
total_manual = st.number_input("Total Estimated Repair Cost", min_value=0.0, format="%.2f")

# Generate PDF
if st.button("Generate PDF Report"):
    # Calculate total
    total_calc = sum([c[3] for c in check_data])
    final_total = total_manual if total_manual > 0 else total_calc

    pdf = InspectionPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Pre-Purchase Vehicle Inspection Report', ln=True, align='C')
    pdf.ln(4)

    # Client & Vehicle Info
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 6, f'Client: {client_name}', ln=0)
    pdf.cell(0, 6, f'Date: {datetime.datetime.now().strftime("%Y-%m-%d")}', ln=1)
    pdf.cell(40, 6, f'Phone: {client_phone}', ln=0)
    pdf.cell(0, 6, f'Inspector: {inspector}', ln=1)
    pdf.cell(80, 6, f'Vehicle: {vehicle_model} ({vehicle_year})', ln=1)
    pdf.cell(0, 6, f'VIN/Reg: {vehicle_vin}', ln=1)
    pdf.ln(4)

    # Checklist Table
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(90, 6, 'Item', border=1)
    pdf.cell(24, 6, 'Status', border=1)
    pdf.cell(58, 6, 'Notes', border=1)
    pdf.cell(18, 6, 'Est Cost', border=1, ln=1)

    pdf.set_font('Arial', '', 9)
    for item, status, notes_text, cost in check_data:
        pdf.cell(90, 6, item[:60], border=1)
        pdf.cell(24, 6, status, border=1)
        pdf.cell(58, 6, notes_text[:150], border=1)
        pdf.cell(18, 6, f'{cost:.2f}', border=1, ln=1)

    pdf.ln(4)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, f'Total Estimated Repair Cost: {final_total:.2f}', ln=1)
    pdf.ln(4)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'Summary / Notes:', ln=1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 6, summary or 'No additional notes provided.')
    pdf.ln(4)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'Recommendation:', ln=1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, recommendation, ln=1)

    pdf.ln(12)
    pdf.cell(0, 6, 'Inspector Signature: ______________________         Client Signature: ______________________', ln=1)

    # Save PDF
    safe_client = ''.join(c for c in client_name if c.isalnum() or c in (' ', '-', '_')).strip() or 'client'
    filename = f"{REPORTS_DIR}/PPI_{safe_client}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)

    st.success(f"PDF report saved: {filename}")
    with open(filename, "rb") as f:
        st.download_button("Download PDF", f, file_name=os.path.basename(filename))
