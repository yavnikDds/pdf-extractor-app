# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# from app import db
# from . import db
db = SQLAlchemy()  # Initialize without app


# db = SQLAlchemy()  # Initialize without app; bind it later in app.py
# db = SQLAlchemy(app)

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
    adr = db.Column(db.Numeric(10,2))
    revpar = db.Column(db.Numeric(10,2))
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

# Bind db to app after models are defined (done in app.py)