from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
from datetime import datetime

app = Flask(__name__)

# Ensure logo exists
LOGO_PATH = "logo.jpeg"

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_report():
    # Collect form data
    client_name = request.form['client_name']
    client_phone = request.form['client_phone']
    car_make = request.form['car_make']
    car_model = request.form['car_model']
    car_year = request.form['car_year']
    inspection_notes = request.form['inspection_notes']

    # Create PDF
    pdf = FPDF()
    pdf.add_page()

    # Add logo
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, 10, 8, 33)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(80)  # move to the right
    pdf.cell(30, 10, "Car Inspection Report", 0, 1, "C")

    # Date
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)

    # Client Info
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Client Information", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Name: {client_name}", ln=True)
    pdf.cell(0, 10, f"Phone: {client_phone}", ln=True)

    # Car Info
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Car Information", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Make: {car_make}", ln=True)
    pdf.cell(0, 10, f"Model: {car_model}", ln=True)
    pdf.cell(0, 10, f"Year: {car_year}", ln=True)

    # Inspection Notes
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Inspection Notes", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, inspection_notes)

    # Save file
    filename = f"inspection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join("reports", filename)

    if not os.path.exists("reports"):
        os.makedirs("reports")

    pdf.output(filepath)

    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
