from flask import Flask, render_template, request, send_file,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import text for raw SQL queries
import tabula
import pandas as pd
import os
import csv
import config

app = Flask(__name__)
app.secret_key = 'The_Secerate_Key'  # Needed for session storage

# table extraction logic
UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded PDFs temporarily
ALLOWED_EXTENSIONS = {'pdf'} # Allowed file extensions
CSV_FOLDER = 'csv_output' # Folder to store output CSVs

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CSV_FOLDER'] = CSV_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Make sure upload and csv folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CSV_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_tables(dfs, csv_path):
    """
    Writes each DataFrame to the CSV file with a blank line separator.
    """
    with open(csv_path, 'w', newline='', encoding='utf-8', errors='replace') as f:
        writer = csv.writer(f)
        for i, df in enumerate(dfs):
            # Convert DataFrame to strings (avoids mixed-type warnings)
            df = df.astype(str)
            
            # Write header
            writer.writerow(df.columns.tolist())
            
            # Write data rows
            for _, row in df.iterrows():
                writer.writerow(row.tolist())
            
            # Add a blank line after each table (except the last one)
            if i < len(dfs) - 1:
                writer.writerow([])
# table extraction logic


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'pdf_file' not in request.files:
            return render_template('index.html', error='No file part')
        file = request.files['pdf_file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        if file and allowed_file(file.filename):
            filename = file.filename
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(pdf_path)

            try:
                dfs = tabula.read_pdf(pdf_path, pages='all', stream=True, guess=True)
                if dfs:
                    csv_filename = filename.rsplit('.', 1)[0] + ".csv"
                    csv_path = os.path.join(app.config['CSV_FOLDER'], csv_filename)
                    
                    # Write tables to CSV with proper formatting
                    format_tables(dfs, csv_path)  # Replace your old formatted_df logic
                    
                    os.remove(pdf_path)
                    session['csv_filename'] = csv_filename  # Store filename in session
                    return render_template('index.html', success=True, csv_filename=csv_filename)
                else:
                    os.remove(pdf_path) # Clean up uploaded PDF after processing (success or failure)
                    return render_template('index.html', error='No tables found in PDF')


            except Exception as e:
                # os.remove(pdf_path) # Clean up uploaded PDF even if error
                return render_template('index.html', error=f'Error processing PDF: {e}')
            # finally:
            #     os.remove(pdf_path) # Clean up uploaded PDF after processing (success or failure)


    return render_template('index.html') # For GET request, just show the upload form


@app.route('/download_csv/<filename>') #connect specific web address to a function and <filename> is a varible part it expect some value
def download_csv(filename):
    csv_path = os.path.join(app.config['CSV_FOLDER'], filename)
    # os is a module. path.join joints a diffrent path with correct slashes, and in small brakets are aguments 
    if os.path.exists(csv_path): # check if file or folder actually exist at this csv_path location
        return send_file(csv_path, as_attachment=True) # This is a function in Flask specifically for sending files back to the user's web browser. as_attachment=True tells the web browser: "Don't try to display this file in the browser. Instead, treat it as a file to be downloaded". 
    else:
        return "CSV file not found."


@app.route('/preview_csv/<filename>')
def preview_csv(filename):
    csv_path = os.path.join(app.config['CSV_FOLDER'], filename)
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)  # Read CSV into a list of lists

        # Determine the maximum number of columns in any row
        max_cols = max(len(row) for row in rows)

        # Pad shorter rows with empty values
        for row in rows:
            while len(row) < max_cols:
                row.append("")
        return render_template("preview.html", table_data=rows)

    return "CSV file not found.", 404

# Test Connection
@app.route('/test_db')
def test_db():
    try:
        db.session.execute(text('SELECT 1'))  # Simple query to check connection
        return "Database Connected Successfully!"
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True) # Run the Flask app in debug mode (for development)