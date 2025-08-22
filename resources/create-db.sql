-- USERS TABLE
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR,
    email VARCHAR,
    phone VARCHAR,
    password_hash VARCHAR,
    role VARCHAR, -- e.g., 'Manager'
    created_at TIMESTAMP
);

-- SUBCONTRACTORS TABLE
CREATE TABLE Subcontractors (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR,
    contact_name VARCHAR,
    email VARCHAR,
    phone VARCHAR,
    address VARCHAR,
    city VARCHAR,
    state VARCHAR,
    created_at TIMESTAMP
);

-- RFQs TABLE
CREATE TABLE RFQs (
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    description TEXT,
    due_date TIMESTAMP,
    status VARCHAR, -- Draft, Open, Closed
    created_at TIMESTAMP,
    manager_id INT REFERENCES Users(id)
);

-- QUOTATIONS TABLE
CREATE TABLE Quotations (
    id SERIAL PRIMARY KEY,
    rfq_id INT REFERENCES RFQs(id),
    subcontractor_id INT REFERENCES Subcontractors(id),
    submitted_at TIMESTAMP,
    estimated_cost DECIMAL,
    notes TEXT
);

-- FILES TABLE
CREATE TABLE Files (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR,
    file_type VARCHAR, -- e.g., pdf, jpg, docx
    file_url VARCHAR,
    uploaded_by INT REFERENCES Users(id),
    quotation_id INT REFERENCES Quotations(id),
    contract_id INT REFERENCES Contracts(id),
    uploaded_at TIMESTAMP
);

-- OCR_LOGS TABLE
CREATE TABLE OCR_Logs (
    id SERIAL PRIMARY KEY,
    file_id INT REFERENCES Files(id),
    extracted_text TEXT,
    status VARCHAR, -- Success, Failed, Partial
    error_message TEXT,
    processed_at TIMESTAMP
);

-- CONTRACTS TABLE
CREATE TABLE Contracts (
    id SERIAL PRIMARY KEY,
    rfq_id INT REFERENCES RFQs(id),
    subcontractor_id INT REFERENCES Subcontractors(id),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    status VARCHAR, -- Active, Completed, Pending
    total_cost DECIMAL,
    created_at TIMESTAMP
);

-- PAYMENTS TABLE
CREATE TABLE Payments (
    id SERIAL PRIMARY KEY,
    contract_id INT REFERENCES Contracts(id),
    payment_date TIMESTAMP,
    amount DECIMAL,
    status VARCHAR, -- Paid, Pending, Overdue
    notes TEXT
);

-- MESSAGES TABLE
CREATE TABLE Messages (
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES Users(id),
    recipient_id INT REFERENCES Subcontractors(id),
    message_text TEXT,
    sent_at TIMESTAMP,
    is_read BOOLEAN
);
