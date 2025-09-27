import sys
import os
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook
from io import StringIO

def extract_table_from_html(html_file, output_file=None):
    """
    Extract table from HTML file and save as Excel (.xlsx).
    
    Args:
        html_file (str): Path to the input HTML file
        output_file (str, optional): Path to the output Excel file. 
                                   If not provided, will use the input filename with .xlsx extension.
    """
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the main results table
    table = soup.find('table', {'id': 'resultsGrid'})
    
    if not table:
        print("Error: Could not find the results table in the HTML.")
        sys.exit(1)
    
    # Convert HTML table to pandas DataFrame using StringIO to avoid FutureWarning
    html_string = str(table)
    df = pd.read_html(StringIO(html_string))[0]
    
    # Set output filename if not provided
    if not output_file:
        base_name = os.path.splitext(html_file)[0]
        output_file = f"{base_name}.xlsx"
    
    # Save to Excel
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Table successfully extracted and saved to {output_file}")
    return df

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_table.py <input_html_file> [output_xlsx_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    extract_table_from_html(input_file, output_file)
