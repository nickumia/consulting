#!/usr/bin/env python3
"""
Agent Data Processing Tool

This script provides a command-line interface to:
1. Extract agent data from HTML to Excel
2. Compare two agent Excel files
3. Run a full pipeline: extract HTML and compare with reference

Usage:
    # Extract HTML to Excel
    python process_agents.py extract input.html [output.xlsx]
    
    # Compare two Excel files
    python process_agents.py compare old.xlsx new.xlsx [report.xlsx]
    
    # Full pipeline: extract and compare
    python process_agents.py pipeline reference.xlsx new.html [report.xlsx]
"""
import sys
import os
from extract_table import extract_table_from_html
from compare_agents import compare_agent_files

def process_pipeline(reference_file, new_html, output_file=None):
    """Full pipeline: extract HTML and compare with reference."""
    # Set default output filename if not provided
    if not output_file:
        base_name = os.path.splitext(new_html)[0]
        output_file = f"{base_name}_comparison.xlsx"
    
    temp_file = "temp_extracted.xlsx"
    
    try:
        # Extract HTML to temporary file
        result = extract_table_from_html(new_html, temp_file)
        if result is None or result.empty:
            print("Error: Failed to extract data from HTML or no data found")
            return None
            
        # Compare with reference
        compare_result = compare_agent_files(reference_file, temp_file, output_file)
        return compare_result
        
    except Exception as e:
        print(f"Error during processing: {e}")
        return None
    finally:
        # Clean up temp file if it exists
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not remove temporary file: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Agent Data Processing Tool
        
Usage:
    # Extract HTML to Excel
    python process_agents.py extract input.html [output.xlsx]
    
    # Compare two Excel files
    python process_agents.py compare old.xlsx new.xlsx [report.xlsx]
    
    # Full pipeline: extract and compare
    python process_agents.py pipeline reference.xlsx new.html [report.xlsx]
    """)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'extract':
        if len(sys.argv) < 3:
            print("Error: Missing input HTML file")
            sys.exit(1)
        extract_table_from_html(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    
    elif command == 'compare':
        if len(sys.argv) < 4:
            print("Error: Missing input files")
            sys.exit(1)
        compare_agent_files(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    
    elif command == 'pipeline':
        if len(sys.argv) < 4:
            print("Error: Missing reference file or HTML input")
            sys.exit(1)
        process_pipeline(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)
