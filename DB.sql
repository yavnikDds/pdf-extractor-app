- CREATE DATABASE table_extractor;
- CREATE USER table_extractor_user WITH ENCRYPTED PASSWORD 'admin123';
- GRANT ALL PRIVILEGES ON DATABASE table_extractor TO table_extractor_user;



CREATE TABLE public.financial_reports (
    id SERIAL PRIMARY KEY,
    report_date DATE NOT NULL,
    revenue NUMERIC(12, 2),
    expenses NUMERIC(12, 2),
    occupancy_rate NUMERIC(5, 2),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.hotel_performance (
    id SERIAL PRIMARY KEY,
    report_date DATE NOT NULL,
    rooms_available INTEGER,
    rooms_occupied INTEGER,
    occupancy_percentage NUMERIC(5, 2),
    adr NUMERIC(10, 2),
    revpar NUMERIC(10, 2),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.quality_evaluations (
    id SERIAL PRIMARY KEY,
    report_date DATE NOT NULL,
    brand_safety_score NUMERIC(5, 2),
    cleanliness_score NUMERIC(5, 2),
    condition_score NUMERIC(5, 2),
    compliance_status VARCHAR(50),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);