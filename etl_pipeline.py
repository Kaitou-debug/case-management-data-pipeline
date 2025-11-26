import pandas as pd
import sqlite3
import os

# --- CONFIGURATION ---
DB_NAME = 'case_management.db'
STATUS_SHEET_FILE = 'data/PW_Young_Men_Status_Sheet.xlsx'
EXPENSE_SHEET_FILE = 'data/July_2025_Expense_Sheet.xlsx'

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}")
    except Exception as e:
        print(e)
    return conn

def transform_status_data(df):
    """
    Cleans and transforms the 'Status Sheet' data.
    - Handles missing dates (forward fill).
    - Extracts numerical scores from 'Level of Growth' text.
    """
    # Standardize column names
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    
    # 1. Fill missing dates (assuming logs are chronological)
    df['date'] = df['date'].fillna(method='ffill')
    
    # 2. Extract numerical score from string "1 (As per questionnaire)"
    # Regex logic: Find the first digit in the string
    df['growth_score'] = df['level_of_growth'].str.extract('(\d+)').fillna(0).astype(int)
    
    # 3. Clean text fields
    df['summary'] = df['summary'].fillna('No Summary Provided')
    
    return df

def transform_expense_data(df):
    """
    Cleans and transforms the 'Expense Sheet' data.
    """
    # Drop rows where 'Amount' is empty (header rows or totals)
    df = df.dropna(subset=['Amount'])
    
    # Ensure Amount is numeric
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0.0)
    
    return df

def run_pipeline():
    conn = create_connection(DB_NAME)
    
    # --- STEP 1: LOAD RAW DATA ---
    # In a real scenario, we loop through all sheets (one per participant)
    # For demo, we assume we loaded one representative sheet
    print("Loading Raw Data...")
    
    # Mocking the load for the repo demonstration if file doesn't exist
    if not os.path.exists(STATUS_SHEET_FILE):
        print("Warning: Source files not found. Creating mock data structure for demonstration.")
        # Create dummy data so the script runs for the recruiter if they try it
        raw_status_data = {
            'Date': ['2025-05-05', None, '2025-05-29'],
            'Summary': ['Initial Call', 'Follow up', 'Meeting at Office'],
            'Case Worker Action': ['Phone Call', 'Phone Call', 'In Person'],
            'Level of Growth': ['1 (As per questionnaire)', '1 (As per questionnaire)', '3']
        }
        df_status = pd.DataFrame(raw_status_data)
    else:
        df_status = pd.read_excel(STATUS_SHEET_FILE)

    # --- STEP 2: TRANSFORM ---
    print("Transforming Data...")
    clean_status = transform_status_data(df_status)
    print(f"Transformed {len(clean_status)} intervention records.")

    # --- STEP 3: LOAD TO SQL ---
    print("Loading to Database...")
    clean_status.to_sql('interventions', conn, if_exists='append', index=False)
    
    print("Pipeline Execution Complete.")
    conn.close()

if __name__ == "__main__":
    run_pipeline()
