**Step 1: Setting Up PostgreSQL**
1. Install PostgreSQL (If Not Installed)
1.1 Open PowerShell & Connect to PostgreSQL
<!-- password is 0000 -->
- psql -U postgres

2. Create a New Database
<!-- after login - Create the Database -->
- CREATE DATABASE table_extractor;

3. Create a User and Grant Permissions
- CREATE USER table_extractor_user WITH ENCRYPTED PASSWORD 'admin123';
- GRANT ALL PRIVILEGES ON DATABASE table_extractor TO table_extractor_user;

**Step 2: Set Up Flask with PostgreSQL**
1. Install Required Packages
<!-- turn on venv and then install the libraries -->
- pip install psycopg2 flask-sqlalchemy

2. Create config.py (Database Configuration)
- New-Item -ItemType File -Name config.py

3. Set Up SQLAlchemy in app.py
<!-- Modify your app.py file: -->
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import text for raw SQL queries
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Test Connection
@app.route('/test_db')
def test_db():
    try:
        db.session.execute(text('SELECT 1'))  # Simple query to check connection
        return "Database Connected Successfully!"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)

**Step 3: Create Database Tables in PostgreSQL**
1. Define Models (models.py)
- Create a new file in your project folder called models.py and add:

from app import db

class FinancialReport(db.Model):
    __tablename__ = 'financial_reports'
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False)
    revenue = db.Column(db.Numeric(12,2))
    expenses = db.Column(db.Numeric(12,2))
    occupancy_rate = db.Column(db.Numeric(5,2))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class HotelPerformance(db.Model):
    __tablename__ = 'hotel_performance'
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False)
    rooms_available = db.Column(db.Integer)
    rooms_occupied = db.Column(db.Integer)
    occupancy_percentage = db.Column(db.Numeric(5,2))
    adr = db.Column(db.Numeric(10,2))  # Average Daily Rate
    revpar = db.Column(db.Numeric(10,2))  # Revenue per Available Room
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class QualityEvaluation(db.Model):
    __tablename__ = 'quality_evaluations'
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False)
    brand_safety_score = db.Column(db.Numeric(5,2))
    cleanliness_score = db.Column(db.Numeric(5,2))
    condition_score = db.Column(db.Numeric(5,2))
    compliance_status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

**Step 3.2: Initialize the Database (Creating Tables in PostgreSQL)**
- After defining the database models in models.py, we need to create these tables inside PostgreSQL.
- we use Flask SQLAlchemy’s create_all() method, which reads the models and generates the necessary tables in the database.

1️⃣ Open PowerShell & Start Python Interactive Shell
- Navigate to your project directory in PowerShell:
- Start the Python interactive shell by running:
    python

2️⃣ Run the Following Commands Inside the Python Shell
    from app import app, db  # Import both the app and db instance
    import models  # Ensure models are loaded

    with app.app_context():  # Create an application context
        db.create_all()  # Create tables inside PostgreSQL

    exit()  # Exit Python shell

3️⃣ Verify the Tables Were Created
- After exiting Python, run the following PostgreSQL command in PowerShell:
    psql -U table_extractor_user -d table_extractor -c "\dt"


**If psql returns "Did not find any relations", it means the tables were not created successfully. Let's troubleshoot and fix it.**

✅ Step 1: Check Database Connection in Python
- Run this in PowerShell:
    python
    from app import app, db
    with app.app_context():  # Set up an application context
    print(db.engine.url)  # Print the database URL
- If the output is something like:
    postgresql://table_extractor_user:yourpassword@localhost/table_extractor
✅ Database URL is correct → Move to Step 2 (Check the database in PostgreSQL).

✅ Step 2: Verify Database Exists in PostgreSQL
- Your database exists, but the tables are still missing. Let's recreate them properly.

✅ Step 3: Recreate the Tables in PostgreSQL
- python
from app import app, db
import models  # Ensure models are loaded

with app.app_context():  # Create an application context
    db.create_all()  # Create the tables




1️⃣ Open PowerShell & Access PostgreSQL
- psql -U table_extractor_user -d table_extractor
