"""
Pre-Purchase Vehicle Inspection (PPI) - Tkinter GUI
Creates a PDF report using fpdf.

Dependencies:
 - Python 3.8+
 - fpdf (pip install fpdf)
 - pillow (optional, for logo) (pip install pillow)

How to use:
 - Run: python pre_purchase_inspection.py
 - Fill client & vehicle details, check items (Pass/Minor/Major), add notes.
 - Click "Generate PDF Report" to save a PDF in the "reports" folder.

This is a single-file app intended to be easy to customize for your shop.
"""

import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fpdf import FPDF

# ---------------------- Configuration ----------------------
SHOP_NAME = "AUTO MAZEN"
SHOP_ADDRESS = "Dawhat Aramoun/Main Street"
SHOP_PHONE = "03 419 833"
LOGO_PATH = "logo.jpeg"  # hardcoded logo file
REPORTS_DIR = "reports"

if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

CHECK_ITEMS = [
    "Engine - Visual & Oil Leaks",
    "Engine - Compression / Idle / Noises",
    "Engine - Belts & Hoses",
    "Fluids - Oil / Coolant / Transmission",
    "Drivetrain - Axles / CV Joints",
    "Emission - Catalytic Converter",
    "Scratch & Dent Check",
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
        # Add shop name and logo
        if LOGO_PATH and os.path.exists(LOGO_PATH):
            try:
                self.image(LOGO_PATH, 10, 8, 30)  # adjusted size
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

# ---------------------- App GUI ----------------------
class PPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Pre-Purchase Vehicle Inspection')
        self.root.geometry('920x640')

        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill='both', expand=True)

        # Top: Client & Vehicle Details
        top = ttk.Frame(frm)
        top.pack(fill='x')

        left = ttk.Frame(top)
        left.pack(side='left', fill='x', expand=True)

        right = ttk.Frame(top)
        right.pack(side='right', fill='x', expand=True)

        # Client info
        ttk.Label(left, text='Client Name:').grid(row=0, column=0, sticky='w')
        self.client_name = ttk.Entry(left, width=30)
        self.client_name.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(left, text='Phone:').grid(row=1, column=0, sticky='w')
        self.client_phone = ttk.Entry(left, width=30)
        self.client_phone.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(left, text='Inspector:').grid(row=2, column=0, sticky='w')
        self.inspector = ttk.Entry(left, width=30)
        self.inspector.grid(row=2, column=1, padx=5, pady=2)

        # Vehicle info
        ttk.Label(right, text='Make / Model:').grid(row=0, column=0, sticky='w')
        self.vehicle_model = ttk.Entry(right, width=30)
        self.vehicle_model.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(right, text='Year:').grid(row=1, column=0, sticky='w')
        self.vehicle_year = ttk.Entry(right, width=30)
        self.vehicle_year.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(right, text='VIN / Reg:').grid(row=2, column=0, sticky='w')
        self.vehicle_vin = ttk.Entry(right, width=30)
        self.vehicle_vin.grid(row=2, column=1, padx=5, pady=2)

        # Middle: Checklist area (scrollable)
        mid = ttk.LabelFrame(frm, text='Inspection Checklist')
        mid.pack(fill='both', expand=True, pady=10)

        canvas = tk.Canvas(mid)
        scrollbar = ttk.Scrollbar(mid, orient='vertical', command=canvas.yview)
        self.checklist_frame = ttk.Frame(canvas)

        self.checklist_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas.create_window((0, 0), window=self.checklist_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Build checklist rows
        self.check_vars = []  # list of (StringVar for status, Entry for notes, Entry for cost)
        for i, item in enumerate(CHECK_ITEMS):
            ttk.Label(self.checklist_frame, text=item).grid(row=i, column=0, sticky='w', padx=6, pady=4)
            status = tk.StringVar(value='Pass')
            cb = ttk.Combobox(self.checklist_frame, textvariable=status, values=['Pass', 'Minor', 'Major'], width=10, state='readonly')
            cb.grid(row=i, column=1, padx=6)
            notes = ttk.Entry(self.checklist_frame, width=50)
            notes.grid(row=i, column=2, padx=6)
            cost = ttk.Entry(self.checklist_frame, width=12)
            cost.insert(0, '0')
            cost.grid(row=i, column=3, padx=6)
            self.check_vars.append((item, status, notes, cost))

        # Bottom: summary, recommendation and buttons
        bottom = ttk.Frame(frm)
        bottom.pack(fill='x')

        ttk.Label(bottom, text='Summary / Notes:').grid(row=0, column=0, sticky='nw')
        self.summary_text = tk.Text(bottom, height=6)
        self.summary_text.grid(row=0, column=1, columnspan=3, padx=6, pady=6, sticky='we')

        ttk.Label(bottom, text='Recommendation:').grid(row=1, column=0, sticky='w')
        self.recommend_var = tk.StringVar(value=RECOMMENDATIONS[0])
        recommend_cb = ttk.Combobox(bottom, textvariable=self.recommend_var, values=RECOMMENDATIONS, state='readonly')
        recommend_cb.grid(row=1, column=1, padx=6, sticky='w')

        ttk.Label(bottom, text='Estimated Total Repair Cost:').grid(row=1, column=2, sticky='e')
        self.total_cost_var = tk.StringVar(value='0')
        self.total_cost_entry = ttk.Entry(bottom, textvariable=self.total_cost_var, width=16)
        self.total_cost_entry.grid(row=1, column=3, sticky='w', padx=6)

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill='x', pady=8)

        gen_btn = ttk.Button(btn_frame, text='Generate PDF Report', command=self.generate_report)
        gen_btn.pack(side='left', padx=6)

        save_btn = ttk.Button(btn_frame, text='Save Data (CSV)', command=self.save_csv)
        save_btn.pack(side='left', padx=6)

        clear_btn = ttk.Button(btn_frame, text='Clear Form', command=self.clear_form)
        clear_btn.pack(side='left', padx=6)

    def calculate_total_from_items(self):
        total = 0.0
        for _, _, _, cost_entry in self.check_vars:
            try:
                v = float(cost_entry.get() or 0)
            except ValueError:
                v = 0.0
            total += v
        return total

    def generate_report(self):
        # Basic validation
        if not self.client_name.get().strip():
            if not messagebox.askyesno('Confirm', 'Client name is empty. Continue?'):
                return

        total_from_items = self.calculate_total_from_items()
        try:
            manual_total = float(self.total_cost_var.get() or 0)
        except ValueError:
            manual_total = 0
        # If manual_total is zero, use calculated
        final_total = manual_total if manual_total > 0 else total_from_items

        # Create PDF
        pdf = InspectionPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Pre-Purchase Vehicle Inspection Report', ln=True, align='C')
        pdf.ln(4)

        # Client & vehicle block
        pdf.set_font('Arial', '', 10)
        pdf.cell(40, 6, f'Client: {self.client_name.get()}', ln=0)
        pdf.cell(0, 6, f'Date: {datetime.datetime.now().strftime("%Y-%m-%d")}', ln=1)
        pdf.cell(40, 6, f'Phone: {self.client_phone.get()}', ln=0)
        pdf.cell(0, 6, f'Inspector: {self.inspector.get()}', ln=1)
        pdf.cell(80, 6, f'Vehicle: {self.vehicle_model.get()} ({self.vehicle_year.get()})', ln=1)
        pdf.cell(0, 6, f'VIN/Reg: {self.vehicle_vin.get()}', ln=1)
        pdf.ln(4)

        # Checklist table header
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(90, 6, 'Item', border=1)
        pdf.cell(24, 6, 'Status', border=1)
        pdf.cell(58, 6, 'Notes', border=1)
        pdf.cell(18, 6, 'Est Cost', border=1, ln=1)

        pdf.set_font('Arial', '', 9)
        for item, status_var, notes_entry, cost_entry in self.check_vars:
            status = status_var.get()
            notes = notes_entry.get()[:150]
            try:
                cost = float(cost_entry.get() or 0)
            except ValueError:
                cost = 0
            # Row layout
            pdf.cell(90, 6, item[:60], border=1)
            pdf.cell(24, 6, status, border=1)
            pdf.cell(58, 6, notes, border=1)
            pdf.cell(18, 6, f'{cost:.2f}', border=1, ln=1)

        pdf.ln(4)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, f'Total Estimated Repair Cost: {final_total:.2f}', ln=1)
        pdf.ln(4)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, 'Summary / Notes:', ln=1)
        pdf.set_font('Arial', '', 10)
        summary = self.summary_text.get('1.0', 'end').strip()
        pdf.multi_cell(0, 6, summary or 'No additional notes provided.')
        pdf.ln(4)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, 'Recommendation:', ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, self.recommend_var.get(), ln=1)

        # Sign area
        pdf.ln(12)
        pdf.cell(0, 6, 'Inspector Signature: ______________________         Client Signature: ______________________', ln=1)

        # Save file
        safe_client = ''.join(c for c in self.client_name.get() if c.isalnum() or c in (' ', '-', '_')).strip()
        if not safe_client:
            safe_client = 'client'
        filename = f"{REPORTS_DIR}/PPI_{safe_client}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        try:
            pdf.output(filename)
            messagebox.showinfo('Saved', f'Report saved as:\n{filename}')
        except Exception as e:
            messagebox.showerror('Error saving', str(e))

    def save_csv(self):
        # Save checklist + metadata to CSV for records
        import csv
        safe_client = ''.join(c for c in self.client_name.get() if c.isalnum() or c in (' ', '-', '_')).strip() or 'client'
        filename = f"{REPORTS_DIR}/PPI_{safe_client}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Client', self.client_name.get()])
                writer.writerow(['Phone', self.client_phone.get()])
                writer.writerow(['Inspector', self.inspector.get()])
                writer.writerow(['Vehicle', self.vehicle_model.get()])
                writer.writerow(['Year', self.vehicle_year.get()])
                writer.writerow(['VIN', self.vehicle_vin.get()])
                writer.writerow([])
                writer.writerow(['Item', 'Status', 'Notes', 'Est Cost'])
                for item, status_var, notes_entry, cost_entry in self.check_vars:
                    writer.writerow([item, status_var.get(), notes_entry.get(), cost_entry.get()])
                writer.writerow([])
                writer.writerow(['Summary', self.summary_text.get('1.0', 'end').strip()])
                writer.writerow(['Recommendation', self.recommend_var.get()])
            messagebox.showinfo('Saved', f'CSV saved as:\n{filename}')
        except Exception as e:
            messagebox.showerror('Error saving CSV', str(e))

    def clear_form(self):
        self.client_name.delete(0, 'end')
        self.client_phone.delete(0, 'end')
        self.inspector.delete(0, 'end')
        self.vehicle_model.delete(0, 'end')
        self.vehicle_year.delete(0, 'end')
        self.vehicle_vin.delete(0, 'end')
        for _, status, notes, cost in self.check_vars:
            status.set('Pass')
            notes.delete(0, 'end')
            cost.delete(0, 'end')
            cost.insert(0, '0')
        self.summary_text.delete('1.0', 'end')
        self.recommend_var.set(RECOMMENDATIONS[0])
        self.total_cost_var.set('0')


if __name__ == '__main__':
    root = tk.Tk()
    app = PPIApp(root)
    root.mainloop()
