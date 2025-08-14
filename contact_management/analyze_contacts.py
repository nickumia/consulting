#!/usr/bin/env python3
"""
Analyze contact lists and find matching entries between two CSV files.
"""
import csv
from datetime import datetime
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

def export_matches_to_csv(contacts1: dict, contacts2: dict, matching_keys: list, output_file: str):
    """
    Export matching records from both contact lists to a CSV file.

    Args:
        contacts1: First contact dictionary
        contacts2: Second contact dictionary
        matching_keys: List of matching keys (phone numbers)
        output_file: Path to output CSV file
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    # Get all unique base field names from both contact dictionaries
    base_fieldnames = set()
    for contact in list(contacts1.values()) + list(contacts2.values()):
        base_fieldnames.update(contact.keys())

    # Create field names with suffixes for both files
    fieldnames = []
    for field in sorted(base_fieldnames):
        fieldnames.append(f"{field}_1")
        fieldnames.append(f"{field}_2")

    # Add source file indicators
    fieldnames.extend(['source_file_1', 'source_file_2'])

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for key in matching_keys:
            # Get records from both files
            record1 = contacts1.get(key, {})
            record2 = contacts2.get(key, {})

            # Create combined record with all fields from both records
            combined = {}

            # Add all fields from first record with _1 suffix
            for k, v in record1.items():
                combined[f"{k}_1"] = v

            # Add all fields from second record with _2 suffix
            for k, v in record2.items():
                combined[f"{k}_2"] = v

            # Add source file indicators
            combined['source_file_1'] = 'Yes'
            combined['source_file_2'] = 'Yes'

            writer.writerow(combined)

    print(f"\nExported {len(matching_keys)} matching records to {output_file}")

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

        # If there are matches, export them to a CSV file
        if results['matches'] > 0:
            # Generate output filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"contact_matches_{timestamp}.csv"

            # Reload the contacts to get full data (since compare_contacts doesn't return them)
            contacts1 = parse_contacts_to_dict(file1)
            contacts2 = parse_contacts_to_dict(file2)

            export_matches_to_csv(
                contacts1,
                contacts2,
                results['matching_keys'],
                output_file
            )

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
