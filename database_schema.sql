-- Database Schema for Case Management System
-- Designed to normalize data from disparate Excel trackers

-- 1. Participants Table (Core Entity)
CREATE TABLE participants (
    participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    joining_date DATE,
    current_status TEXT, -- Active, Transitioned, etc.
    risk_level TEXT -- Derived from assessments
);

-- 2. Interventions Table (From "Status Sheet")
-- Tracks every interaction, call, or meeting with a participant
CREATE TABLE interventions (
    intervention_id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id INTEGER,
    interaction_date DATE,
    summary TEXT,
    case_worker_action TEXT,
    location TEXT, -- e.g., "Pathways Office", "Phone Call"
    level_of_growth_score INTEGER, -- Numerical score extracted from "1 (As per questionnaire)"
    notes TEXT,
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id)
);

-- 3. Program Expenses Table (From "Expense Sheet")
-- Tracks financial resources allocated to specific program categories
CREATE TABLE program_expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id INTEGER, -- Nullable if expense is general (e.g., Office Supplies)
    expense_date DATE,
    program_category TEXT, -- e.g., "Care Coordination", "Medical", "Social"
    details TEXT,
    amount DECIMAL(10, 2),
    staff_member TEXT, -- Who incurred the expense
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id)
);

-- 4. Assessments Table (Structured Data)
-- Stores longitudinal scores from CANS or Level of Growth assessments
CREATE TABLE assessments (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id INTEGER,
    assessment_date DATE,
    assessment_type TEXT, -- "CANS", "Level of Growth"
    total_score INTEGER,
    domain_scores JSON, -- Storing breakdown of scores
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id)
);
