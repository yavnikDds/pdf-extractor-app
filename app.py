from flask import Flask, render_template, request, send_file, session, jsonify
from datetime import datetime
from sqlalchemy import text  # Import text for raw SQL queries
from flask_sqlalchemy import SQLAlchemy
import tabula
import pandas as pd
import os
import csv
import config

# from models import create_app, db

from model import FinancialReport, HotelPerformance, QualityEvaluation, db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Bind db to app
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
            writer.writerow(df.columns.tolist())
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
                dfs = tabula.read_pdf(pdf_path, pages='all', stream=True)
                if dfs:
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
    max_cols = max(len(row) for row in rows) if rows else 0
    for row in rows:
        while len(row) < max_cols:
            row.append("")
    return render_template("preview.html", table_data=rows, filename=filename)

def save_to_database(edited_data, table_type):
    try:
        if table_type == "financial_reports":
            for row in edited_data[1:]:
                if len(row) >= 4:
                    report = FinancialReport(
                        report_date=datetime.strptime(row[0], '%Y-%m-%d').date(),
                        revenue=float(row[1]) if row[1] else None,
                        expenses=float(row[2]) if row[2] else None,
                        occupancy_rate=float(row[3]) if row[3] else None
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
        return f"Error saving to database: {str(e)}"

@app.route('/test_db')
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

# Add this new endpoint below your existing routes
@app.route('/insert_to_database', methods=['POST'])
def insert_to_database():
    try:
        data = request.get_json()
        headers = data['headers']
        edited_data = data['data']

        # Split data into tables based on blank rows
        tables = []
        current_table = []
        for row in edited_data:
            is_blank = all(cell in ('', None) for cell in row)
            if is_blank and current_table:
                tables.append(current_table)
                current_table = []
            elif not is_blank:
                current_table.append(row)
        if current_table:
            tables.append(current_table)

        if not tables:
            return jsonify({"error": "No valid tables found in the data"}), 400

        # Process the first table
        table_data = tables[0]  # Data rows only (headers are separate)

        # Expected FinancialReport columns
        expected_headers = {'report_date', 'revenue', 'expenses', 'occupancy_rate'}
        filtered_headers = [h for h in headers if h]  # Ignore blank headers
        if not all(h in expected_headers for h in filtered_headers):
            missing = expected_headers - set(filtered_headers)
            return jsonify({"error": f"Headers must match FinancialReport fields. Missing: {missing}"}), 400

        # Prepare data for save_to_database
        formatted_data = [headers] + table_data
        result = save_to_database(formatted_data, "financial_reports")
        if result == "success":
            return jsonify({"message": "Data inserted successfully"}), 200
        else:
            return jsonify({"error": result}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
if __name__ == '__main__':
    app.run(debug=True)
