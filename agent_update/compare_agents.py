import pandas as pd
import sys
import os
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def compare_agent_files(old_file, new_file, output_file=None):
    """
    Compare two agent Excel files and generate a report with new, deleted, and updated agents.
    
    Args:
        old_file (str): Path to the older version Excel file
        new_file (str): Path to the newer version Excel file
        output_file (str, optional): Path to save the comparison report.
                                   If not provided, will use a default name.
    """
    # Read both Excel files
    try:
        df_old = pd.read_excel(old_file, engine='openpyxl')
        df_new = pd.read_excel(new_file, engine='openpyxl')
    except Exception as e:
        print(f"Error reading files: {e}")
        sys.exit(1)
    
    # Function to find the code column name
    def get_code_column(df):
        for col in df.columns:
            if col.strip() == 'Code #':
                return col
        return None
    
    # Get the actual code column names
    code_col_old = get_code_column(df_old)
    code_col_new = get_code_column(df_new)
    
    if not code_col_old or not code_col_new:
        print("Error: Could not find 'Code #' column in one or both files.")
        print(f"Old file columns: {df_old.columns.tolist()}")
        print(f"New file columns: {df_new.columns.tolist()}")
        sys.exit(1)
    
    # Set the code column as index for both dataframes
    df_old = df_old.set_index(code_col_old)
    df_new = df_new.set_index(code_col_new)
    
    # Clean up the index (remove any whitespace)
    df_old.index = df_old.index.astype(str).str.strip()
    df_new.index = df_new.index.astype(str).str.strip()
    
    # Find new agents (in new but not in old)
    new_agents = df_new[~df_new.index.isin(df_old.index)]
    
    # Find deleted agents (in old but not in new)
    deleted_agents = df_old[~df_old.index.isin(df_new.index)]
    
    # Find common agents
    common_agents = df_new[df_new.index.isin(df_old.index)]
    
    # Find updated agents (common agents with different data)
    updated_agents = []
    for agent_code in common_agents.index:
        old_row = df_old.loc[agent_code]
        new_row = df_new.loc[agent_code]
        
        # Compare rows, ignoring index and any NaN values
        if not old_row.equals(new_row):
            # Create a combined row showing both old and new values
            combined_row = new_row.copy()
            for col in new_row.index:
                if col in old_row and old_row[col] != new_row[col]:
                    combined_row[col] = f"{old_row[col]} → {new_row[col]}"
            updated_agents.append(combined_row)
    
    # Convert list of updated agents to DataFrame
    df_updated = pd.DataFrame(updated_agents) if updated_agents else pd.DataFrame()
    
    # Set output filename if not provided
    if not output_file:
        base_name = os.path.splitext(new_file)[0]
        output_file = f"{base_name}_comparison.xlsx"
    
    # Create Excel writer object
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Write each DataFrame to a different worksheet
        if not new_agents.empty:
            new_agents.to_excel(writer, sheet_name='New Agents')
        if not deleted_agents.empty:
            deleted_agents.to_excel(writer, sheet_name='Deleted Agents')
        if not df_updated.empty:
            df_updated.to_excel(writer, sheet_name='Updated Agents')
    
    print(f"Comparison report generated: {output_file}")
    return output_file

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compare_agents.py <old_file.xlsx> <new_file.xlsx> [output_file.xlsx]")
        sys.exit(1)
    
    old_file = sys.argv[1]
    new_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    for file_path in [old_file, new_file]:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)
    
    compare_agent_files(old_file, new_file, output_file)
