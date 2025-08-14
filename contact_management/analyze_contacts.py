#!/usr/bin/env python3
"""
Analyze contact lists and find matching entries between two CSV files.
"""
import os
import sys
from parse_contacts import parse_contacts_to_dict

def compare_contacts(file1: str, file2: str) -> dict:
    """
    Compare two contact lists and return analysis of matches.
    
    Args:
        file1: Path to first CSV file
        file2: Path to second CSV file
        
    Returns:
        Dictionary containing analysis results
    """
    print(f"\n{'='*50}")
    print("Analyzing contact lists...")
    print(f"File 1: {file1}")
    print(f"File 2: {file2}")
    print("="*50)
    
    # Parse both contact lists
    print("\nParsing first file...")
    contacts1 = parse_contacts_to_dict(file1)
    print(f"Found {len(contacts1)} contacts in first file")
    
    print("\nParsing second file...")
    contacts2 = parse_contacts_to_dict(file2)
    print(f"Found {len(contacts2)} contacts in second file")
    
    # Find matching keys
    keys1 = set(contacts1.keys())
    keys2 = set(contacts2.keys())
    
    # Calculate matches and differences
    matches = keys1.intersection(keys2)
    only_in_file1 = keys1 - keys2
    only_in_file2 = keys2 - keys1
    
    # Prepare results
    results = {
        'file1': file1,
        'file2': file2,
        'total_file1': len(contacts1),
        'total_file2': len(contacts2),
        'matches': len(matches),
        'only_in_file1': len(only_in_file1),
        'only_in_file2': len(only_in_file2),
        'match_percentage': (len(matches) / max(len(contacts1), 1)) * 100,
        'matching_keys': sorted(list(matches)),
        'unique_to_file1': sorted(list(only_in_file1)),
        'unique_to_file2': sorted(list(only_in_file2))
    }
    
    return results

def print_analysis(results: dict):
    """Print the analysis results in a readable format."""
    print("\n" + "="*50)
    print("CONTACT LIST COMPARISON RESULTS")
    print("="*50)
    print(f"\nFile 1: {results['file1']}")
    print(f"File 2: {results['file2']}")
    
    print("\nSummary:")
    print(f"- Total contacts in File 1: {results['total_file1']}")
    print(f"- Total contacts in File 2: {results['total_file2']}")
    print(f"- Matching contacts: {results['matches']} ({results['match_percentage']:.1f}% of File 1)")
    print(f"- Contacts only in File 1: {results['only_in_file1']}")
    print(f"- Contacts only in File 2: {results['only_in_file2']}")
    
    if results['matches'] > 0:
        print("\nMatching contacts:")
        for key in results['matching_keys'][:10]:  # Show first 10 matches
            print(f"  - {key}")
        if len(results['matching_keys']) > 10:
            print(f"  ... and {len(results['matching_keys']) - 10} more")
    
    if results['only_in_file1'] > 0:
        print(f"\nContacts only in {os.path.basename(results['file1'])}:")
        for key in results['unique_to_file1'][:5]:  # Show first 5 unique to file1
            print(f"  - {key}")
        if len(results['unique_to_file1']) > 5:
            print(f"  ... and {len(results['unique_to_file1']) - 5} more")
    
    if results['only_in_file2'] > 0:
        print(f"\nContacts only in {os.path.basename(results['file2'])}:")
        for key in results['unique_to_file2'][:5]:  # Show first 5 unique to file2
            print(f"  - {key}")
        if len(results['unique_to_file2']) > 5:
            print(f"  ... and {len(results['unique_to_file2']) - 5} more")

def main():
    """Main function to run the contact comparison."""
    if len(sys.argv) != 3:
        print("Usage: python analyze_contacts.py <file1.csv> <file2.csv>")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    if not os.path.exists(file1) or not os.path.exists(file2):
        print("Error: One or both files do not exist")
        sys.exit(1)
    
    try:
        results = compare_contacts(file1, file2)
        print_analysis(results)
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
