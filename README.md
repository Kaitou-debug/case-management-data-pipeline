# Case Management Data Pipeline 🛠️

## 🚀 Project Overview

This project demonstrates an **ETL (Extract, Transform, Load)** pipeline built to modernize a manual case management system.

The original system relied on disconnected Excel workbooks (`Status Sheets`, `Expense Logs`, `Case History Docs`) to track 20+ participants. This pipeline ingests that unstructured data, cleans it, and loads it into a centralized **SQL Relational Database** to enable longitudinal analysis.

## 💼 Business Context

* **Role:** Care Coordination Lead

* **Problem:** Data was siloed in 15+ separate Excel files (one per participant), making it impossible to query aggregate trends (e.g., *"Show me total medical spend vs. growth score for all participants"*).

* **Solution:** Built a Python-based pipeline to consolidate data into a single source of truth.

## ⚙️ Technical Architecture

### 1. Data Sources

* **Longitudinal Status Sheets:** Tracking daily interventions, dates, and "Level of Growth" scores.

* **Expense Trackers:** Categorized spending (Medical, Education, Wellness) per participant.

* **Unstructured Case Notes:** Word documents containing qualitative assessments.

### 2. ETL Logic (`etl_pipeline.py`)

* **Extract:** Uses `pandas` to read multi-tab Excel files.

* **Transform:**

  * **Data Cleaning:** Forward-fills missing dates in log entries.

  * **Feature Extraction:** Parses the "Level of Growth" column (e.g., converting strings like *"1 (As per questionnaire)"* -> Integer `1`).

  * **Normalization:** Maps inconsistent location names (e.g., "Pathways Office" vs "Office").

* **Load:** Writes cleaned data into a `SQLite` relational database using `SQLAlchemy`.

### 3. Database Schema (`database_schema.sql`)

The database is designed with 3 core tables:

* `participants`: Master list of clients.

* `interventions`: Transactional table of every interaction (linked by `participant_id`).

* `program_expenses`: Financial transactions linked to specific program categories.

## 📊 Key Insights Enabled

Once the data is in SQL, we can run complex queries such as:

* *Correlation between "Frequency of Interventions" and "Level of Growth" scores.*

* *Monthly burn rate per Program Category (Care Coordination vs. Medical).*

* *Participant retention rates based on initial risk assessment scores.*

## 💻 How to Run

1. Install dependencies: `pip install pandas sqlalchemy openpyxl`

2. Place raw Excel files in the `/data` folder.

3. Run the pipeline: `python etl_pipeline.py`

*Note: The code in this repository handles sanitized/mock data structures that mirror the actual production environment used at Interserve India.*
