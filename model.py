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
    Region = db.Column(db.String(50), nullable=False)  # For "West", etc.
    Hotels = db.Column(db.Numeric(12,2))               # For 11.0, etc.
    Hotels_percent = db.Column(db.Numeric(12,2))       # For 28% → 28.0, etc. (renamed from Hotels_)
    Rooms = db.Column(db.Numeric(10,2))                # For 1337.0, etc.
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Add this at the end of model.py (after existing models)
class FinancialRecord(db.Model):
    __tablename__ = 'financial_records'
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(50), nullable=False)  # e.g., "JAN - DEC 2019"
    category = db.Column(db.String(50))  # e.g., "Income" or "Expenses", nullable
    header = db.Column(db.String(100), nullable=False)  # e.g., "cupboard_income"
    value = db.Column(db.Numeric(15,2))  # e.g., 78248.28
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class FinancialStatement(db.Model):
    __tablename__ = 'financial_statements'
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    administration = db.Column(db.Numeric(15,2))  # For Adminstration (corrected typo)
    cupboard_income = db.Column(db.Numeric(15,2))
    gain_on_sale = db.Column(db.Numeric(15,2))
    guest_laundry = db.Column(db.Numeric(15,2))
    miscellaneous_income = db.Column(db.Numeric(15,2))
    room_sales_non_taxable = db.Column(db.Numeric(15,2))
    room_sales_taxable = db.Column(db.Numeric(15,2))
    telephone_income = db.Column(db.Numeric(15,2))
    vending = db.Column(db.Numeric(15,2))
    total_income = db.Column(db.Numeric(15,2))
    advertising = db.Column(db.Numeric(15,2))
    amortization_expenses = db.Column(db.Numeric(15,2))
    bad_debt = db.Column(db.Numeric(15,2))
    bank_service_charges = db.Column(db.Numeric(15,2))
    bonuses = db.Column(db.Numeric(15,2))
    carpet_cleaning = db.Column(db.Numeric(15,2))
    cash_over_short = db.Column(db.Numeric(15,2))
    contract_labor = db.Column(db.Numeric(15,2))
    costs_guests_laundry = db.Column(db.Numeric(15,2))
    credit_card_charges = db.Column(db.Numeric(15,2))
    depreciation_expense = db.Column(db.Numeric(15,2))
    dues_and_subscriptions = db.Column(db.Numeric(15,2))
    equipment_rental = db.Column(db.Numeric(15,2))
    feasibility = db.Column(db.Numeric(15,2))
    food_cost = db.Column(db.Numeric(15,2))
    franchise_fees = db.Column(db.Numeric(15,2))
    franchise_tax = db.Column(db.Numeric(15,2))
    garbage = db.Column(db.Numeric(15,2))
    insurance = db.Column(db.Numeric(15,2))
    interest_expense = db.Column(db.Numeric(15,2))
    landscaping = db.Column(db.Numeric(15,2))
    laundry_supplies = db.Column(db.Numeric(15,2))
    licenses_and_permits = db.Column(db.Numeric(15,2))
    maintenance_contracts = db.Column(db.Numeric(15,2))
    maintenance_supplies = db.Column(db.Numeric(15,2))
    management_fees = db.Column(db.Numeric(15,2))
    miscellaneous = db.Column(db.Numeric(15,2))
    office_expenses = db.Column(db.Numeric(15,2))
    payroll = db.Column(db.Numeric(15,2))
    fica = db.Column(db.Numeric(15,2))
    front_desk = db.Column(db.Numeric(15,2))
    futa_and_twc = db.Column(db.Numeric(15,2))
    head_houskeeping = db.Column(db.Numeric(15,2))
    houskeeping = db.Column(db.Numeric(15,2))
    laundry = db.Column(db.Numeric(15,2))
    maint_security = db.Column(db.Numeric(15,2))
    maintenance = db.Column(db.Numeric(15,2))
    marketing = db.Column(db.Numeric(15,2))
    van_drivers = db.Column(db.Numeric(15,2))
    total_payroll = db.Column(db.Numeric(15,2))
    pest_control = db.Column(db.Numeric(15,2))
    pool_supplies = db.Column(db.Numeric(15,2))
    professional_fees = db.Column(db.Numeric(15,2))
    legal_fees = db.Column(db.Numeric(15,2))
    total_professional_fees = db.Column(db.Numeric(15,2))
    rental_storage = db.Column(db.Numeric(15,2))
    repairs = db.Column(db.Numeric(15,2))
    room_supplies = db.Column(db.Numeric(15,2))
    satellite_tv = db.Column(db.Numeric(15,2))
    security = db.Column(db.Numeric(15,2))
    taxes_property = db.Column(db.Numeric(15,2))
    telephone = db.Column(db.Numeric(15,2))
    entertainment = db.Column(db.Numeric(15,2))
    meals = db.Column(db.Numeric(15,2))
    van_shuttle_cost = db.Column(db.Numeric(15,2))
    total_transportation = db.Column(db.Numeric(15,2))
    travel_agent_commission = db.Column(db.Numeric(15,2))
    uniforms = db.Column(db.Numeric(15,2))
    utilities = db.Column(db.Numeric(15,2))
    workmen_comp = db.Column(db.Numeric(15,2))
    total_expenses = db.Column(db.Numeric(15,2))
    net_operating_income = db.Column(db.Numeric(15,2))
    net_income = db.Column(db.Numeric(15,2))
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