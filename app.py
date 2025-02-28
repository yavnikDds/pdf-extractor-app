from flask import Flask, render_template, request, send_file, session, jsonify
from datetime import datetime
from sqlalchemy import text  # Import text for raw SQL queries
from flask_sqlalchemy import SQLAlchemy
# import tabula
import camelot
import pandas as pd
import os
import csv
import config

# from models import create_app, db

from model import FinancialReport, HotelPerformance, QualityEvaluation, db, FinancialRecord, FinancialStatement

# Add this at the top of app.py, after imports but before create_app
FIELD_OPTIONS = {
    'administration': 'Adminstration',
    'cupboard_income': 'Cupboard Income',
    'gain_on_sale': 'Gain on Sale',
    'guest_laundry': 'Guest Laundry',
    'miscellaneous_income': 'Miscellaneous Income',
    'room_sales_non_taxable': 'Room Sales -Non Taxable',
    'room_sales_taxable': 'Room Sales Taxable',
    'telephone_income': 'Telephone Income',
    'vending': 'Vending',
    'total_income': 'Total Income',
    'advertising': 'Advertising',
    'amortization_expenses': 'Amortization Expenses',
    'bad_debt': 'Bad Debt',
    'bank_service_charges': 'Bank Service Charges',
    'bonuses': 'Bonuses',
    'carpet_cleaning': 'Carpet Cleaning',
    'cash_over_short': 'Cash Over / Short',
    'contract_labor': 'Contract Labor',
    'costs_guests_laundry': 'Costs Guests Laundry',
    'credit_card_charges': 'Credit Card Charges',
    'depreciation_expense': 'Depreciation Expense',
    'dues_and_subscriptions': 'Dues and Subscriptions',
    'equipment_rental': 'Equipment Rental',
    'feasibility': 'Feasibility',
    'food_cost': 'Food Cost',
    'franchise_fees': 'Franchise Fees',
    'franchise_tax': 'Franchise Tax',
    'garbage': 'Garbage',
    'insurance': 'Insurance',
    'interest_expense': 'Interest Expense',
    'landscaping': 'Landscaping',
    'laundry_supplies': 'Laundry Supplies',
    'licenses_and_permits': 'Licenses and Permits',
    'maintenance_contracts': 'Maintenance Contracts',
    'maintenance_supplies': 'Maintenance Supplies',
    'management_fees': 'Management Fees',
    'miscellaneous': 'Miscellaneous',
    'office_expenses': 'Office Expenses',
    'payroll': 'Payroll',
    'fica': 'Fica',
    'front_desk': 'Front Desk',
    'futa_and_twc': 'Futa & Twc',
    'head_houskeeping': 'Head Houskeeping',
    'houskeeping': 'Houskeeping',
    'laundry': 'Laundry',
    'maint_security': 'Maint-Security',
    'maintenance': 'Maintenance',
    'marketing': 'Marketing',
    'van_drivers': 'Van Drivers',
    'total_payroll': 'Total Payroll',
    'pest_control': 'Pest Control',
    'pool_supplies': 'Pool Supplies',
    'professional_fees': 'Professional Fees',
    'legal_fees': 'Legal Fees',
    'total_professional_fees': 'Total Professional Fees',
    'rental_storage': 'Rental-Storage',
    'repairs': 'Repairs',
    'room_supplies': 'Room Supplies',
    'satellite_tv': 'Satillite T.V',
    'security': 'Security',
    'taxes_property': 'Taxes-Property',
    'telephone': 'Telephone',
    'entertainment': 'Entertainment',
    'meals': 'Meals',
    'van_shuttle_cost': 'Van/Schuttle Cost',
    'total_transportation': 'Total Transportation',
    'travel_agent_commission': 'Travel agent Commission',
    'uniforms': 'Uniforms',
    'utilities': 'Utilities',
    'workmen_comp': 'Workmen Comp',
    'total_expenses': 'Total Expenses',
    'net_operating_income': 'NET OPERATING INCOME',
    'net_income': 'NET INCOME'
}

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app
app = create_app()


app.secret_key = 'The_Secret_Key'  # Needed for session storage

# Table extraction logic
UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded PDFs temporarily
CSV_FOLDER = 'csv_output'  # Folder to store output CSVs
ALLOWED_EXTENSIONS = {'pdf'}  # Allowed file extensions

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CSV_FOLDER'] = CSV_FOLDER

# Create tables if they don’t exist
with app.app_context():
    db.create_all()

# Ensure upload and CSV folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CSV_FOLDER, exist_ok=True)

# check if file-type is pdf or not.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_tables(dfs, csv_path):
    """
    Writes each DataFrame to the CSV file with a blank line separator.
    """
    with open(csv_path, 'w', newline='', encoding='utf-8', errors='replace') as f:
        writer = csv.writer(f)
        for i, df in enumerate(dfs):
            df = df.astype(str)
            # writer.writerow(df.columns.tolist())
            for _, row in df.iterrows():
                writer.writerow(row.tolist())
            if i < len(dfs) - 1:
                writer.writerow([])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return render_template('index.html', error='No file part')
        file = request.files['pdf_file']
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        if file and allowed_file(file.filename):
            filename = file.filename
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(pdf_path)
            try:
                # dfs = tabula.read_pdf(pdf_path, pages='all', stream=True)
                tables = camelot.read_pdf(pdf_path, pages='all', flavor="stream")
                if tables:
                    # Convert TableList to list of DataFrames
                    dfs = [table.df for table in tables]
                    csv_filename = filename.rsplit('.', 1)[0] + ".csv"
                    csv_path = os.path.join(app.config['CSV_FOLDER'], csv_filename)
                    format_tables(dfs, csv_path)
                    os.remove(pdf_path)
                    session['csv_filename'] = csv_filename
                    return render_template('index.html', success=True, csv_filename=csv_filename)
                else:
                    os.remove(pdf_path)
                    return render_template('index.html', error='No tables found in PDF')
            except Exception as e:
                return render_template('index.html', error=f'Error processing PDF: {e}')
    return render_template('index.html')

@app.route('/download_csv/<filename>')
def download_csv(filename):
    csv_path = os.path.join(app.config['CSV_FOLDER'], filename)
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True)
    else:
        return "CSV file not found."

@app.route('/preview_csv/<filename>', methods=['GET', 'POST'])
def preview_csv(filename):
    csv_path = os.path.join(app.config['CSV_FOLDER'], filename)
    if not os.path.exists(csv_path):
        return "CSV file not found.", 404
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    # No need to pad rows here; let Handsontable handle it
    print(f"Clicked on preview - {filename}")
    print("Preview data sent:", rows[:5])  # Debug what’s sent to template
    return render_template("preview.html", table_data=rows, filename=filename, FIELD_OPTIONS=FIELD_OPTIONS)
# Ensure clean_numeric is present (add if missing)
def clean_numeric(value):
    if not value or value.lower() == 'nan':
        return None
    try:
        return float(value.replace('%', '').replace(',', ''))
    except (ValueError, TypeError):
        return None


# Add this above save_to_database (e.g., after clean_numeric)
def normalize_header(header):
    """
    Convert a CSV header (e.g., 'Cupboard Income') to a database-friendly name (e.g., 'cupboard_income').
    """
    if not header or header.lower() == 'nan':
        return ''
    # Replace spaces and special characters with underscores, lowercase everything
    normalized = header.lower().replace(' ', '_').replace('-', '_').replace('/', '_').replace('&', 'and')
    # Remove any remaining special characters (keep alphanumeric and underscores)
    normalized = ''.join(c for c in normalized if c.isalnum() or c == '_')
    # Strip leading/trailing underscores
    return normalized.strip('_')

    
# Replace the existing save_to_database function
def save_to_database(edited_data, table_type):
    try:
        if table_type == "financial_reports":
            for row in edited_data[1:]:  # Skip header row
                if len(row) >= 4:
                    report = FinancialReport(
                        Region=row[0] if row[0] and row[0].lower() != 'nan' else '',
                        Hotels=clean_numeric(row[1]),
                        Hotels_percent=clean_numeric(row[2]),
                        Rooms=clean_numeric(row[3])
                    )
                    db.session.add(report)
        elif table_type == "hotel_performance":
            for row in edited_data[1:]:
                if len(row) >= 6:
                    performance = HotelPerformance(
                        report_date=datetime.strptime(row[0], '%Y-%m-%d').date(),
                        rooms_available=int(row[1]) if row[1] else None,
                        rooms_occupied=int(row[2]) if row[2] else None,
                        occupancy_percentage=float(row[3]) if row[3] else None,
                        adr=float(row[4]) if row[4] else None,
                        revpar=float(row[5]) if row[5] else None
                    )
                    db.session.add(performance)
        elif table_type == "quality_evaluations":
            for row in edited_data[1:]:
                if len(row) >= 5:
                    evaluation = QualityEvaluation(
                        report_date=datetime.strptime(row[0], '%Y-%m-%d').date(),
                        brand_safety_score=float(row[1]) if row[1] else None,
                        cleanliness_score=float(row[2]) if row[2] else None,
                        condition_score=float(row[3]) if row[3] else None,
                        compliance_status=row[4] if row[4] else None
                    )
                    db.session.add(evaluation)
        db.session.commit()
        return "success"
    except Exception as e:
        db.session.rollback()
        return f"Error saving to database: {str(e)}"@app.route('/test_db')
        
def test_db():
    try:
        db.session.execute(text('SELECT 1'))
        return "Database Connected Successfully!"
    except Exception as e:
        return str(e)

# Replace the existing save_edited_csv function
@app.route('/save_edited_csv', methods=['POST'])
def save_edited_csv():
    try:
        data = request.get_json()
        filename = data['filename']
        headers = data['headers']
        edited_data = data['data']

        # Create a new filename with a timestamp to avoid overwriting
        print(filename)
        base_name = filename.rsplit('.', 1)[0]
        new_filename = f"{base_name}_edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_path = os.path.join(app.config['CSV_FOLDER'], new_filename)

        # Write headers and data to the new CSV
        with open(csv_path, 'w', newline='', encoding='utf-8', errors='replace') as f:
            writer = csv.writer(f)
            writer.writerow(headers)  # Write headers first
            for row in edited_data:
                writer.writerow(row)  # Write each data row

        return jsonify({"message": "Data saved successfully", "filename": new_filename}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/insert_to_database', methods=['POST'])
def insert_to_database():
    try:
        data = request.get_json()
        headers = data['headers']
        edited_data = data['data']
        filename = data['filename']  # Get filename from payload

        print("Headers from Handsontable:", headers)
        print("Edited data from Handsontable:", edited_data[:5])

        # Find the period row (look for a row with period-like strings)
        period_row = None
        for row in edited_data:
            non_empty = [x for x in row if x]
            if len(non_empty) >= 2 and all('DEC' in str(p) for p in non_empty if p):  # Check for "DEC" in periods
                period_row = row
                break
        if not period_row:
            return jsonify({"error": "No period headers found"}), 400
        periods = [p for p in period_row if p and 'DEC' in p]  # Filter for period strings
        print("Extracted periods:", periods)

        # Process the remaining rows for categories and data, collect row headers
        categories = {}
        current_category = None
        row_headers = []
        for row in edited_data:
            non_empty = [x for x in row if x]
            if len(non_empty) == 1 and not non_empty[0].startswith('Total'):
                # Category title (e.g., "Income" or "Expenses")
                current_category = non_empty[0]
                categories[current_category] = []
            elif current_category and len(non_empty) > 1:
                # Data row (e.g., "Cupboard Income", "78,248.28", "65,906.55")
                header = row[0]
                values = row[1:len(periods) + 1]  # Match values to periods
                if header.startswith('Total'):
                    # Store totals but don’t end category unless explicitly needed
                    if current_category:
                        categories[current_category].append((header, values))
                else:
                    categories[current_category].append((header, values))
                    if header not in row_headers and not header.startswith('Total'):
                        row_headers.append(header)

        # Remove duplicates and sort
        row_headers = sorted(list(set(row_headers)))

        print("Parsed categories and data:")
        for category, rows in categories.items():
            print(f"Category: {category}")
            for header, values in rows:
                print(f"  Header: {header}, Values: {values}")

        # Return row headers for field mapping
        return jsonify({
            "message": "Data parsed successfully",
            "filename": filename,
            "row_headers": row_headers,
            "periods": periods
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/process_mapping', methods=['POST'])
def process_mapping():
    try:
        data = request.get_json()
        filename = data['filename']
        mappings = data['mappings']

        csv_path = os.path.join(app.config['CSV_FOLDER'], filename)
        if not os.path.exists(csv_path):
            return jsonify({"error": "CSV file not found"}), 404

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Skip the first line (A,B,C,D) and period row, then extract period row
        if len(rows) < 2:
            return jsonify({"error": "Not enough data to process"}), 400
        period_row = rows[1]  # ['', 'JAN - DEC 2019', 'JAN - DEC 2018 (PY)', '']
        periods = [p for p in period_row if p]

        # Process categories and data
        categories = {}
        current_category = None
        for row in rows[2:]:  # Skip A,B,C,D and period row
            non_empty = [x for x in row if x]
            if len(non_empty) == 1 and not non_empty[0].startswith('Total'):
                # Category title (e.g., "Income" or "Expenses")
                current_category = non_empty[0]
                categories[current_category] = []
            elif current_category and len(non_empty) > 1:
                header = row[0]
                values = row[1:len(periods) + 1]
                if header.startswith('Total'):
                    # Store totals but don’t set as category
                    if current_category:
                        categories[current_category].append((header, values))
                else:
                    categories[current_category].append((header, values))

        # Insert into database using mappings, ensuring both periods
        records = []
        for category, rows in categories.items():
            for header, values in rows:
                db_field = mappings.get(header, '')
                if db_field and db_field in FIELD_OPTIONS:
                    norm_field = db_field
                    for i, period in enumerate(periods):
                        value = clean_numeric(values[i]) if i < len(values) else None
                        # Insert even if value is None to ensure both periods are represented
                        statement_kwargs = {'period': period, 'category': category}
                        statement_kwargs[norm_field] = value
                        statement = FinancialStatement(**statement_kwargs)
                        records.append(statement)

        db.session.bulk_save_objects(records)
        db.session.commit()

        return jsonify({"message": "Data imported successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500        

if __name__ == '__main__':
    app.run(debug=True)
