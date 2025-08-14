import csv
import os
from typing import Dict, Any

def munge_name(first_name: str, last_name: str) -> str:
    """Munge a name into a format that can be used as a key."""
    if first_name == "" or last_name == "":
        return None
    first_name = first_name.replace(" ", "")
    last_name = last_name.replace(" ", "")
    return f"{first_name.lower()}_{last_name.lower()}"

def parse_contacts_to_dict(csv_path: str) -> Dict[str, Dict[str, str]]:
    """
    Parse a CSV file into a dictionary with '{first}_{last}' as keys.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        Dictionary with '{first}_{last}' as keys and contact info as values
    """
    contacts = {}
    
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Skip rows that don't have at least first or last name
                if not row.get('First Name') and not row.get('Last Name'):
                    continue
                    
                # Clean and format names
                name = munge_name(row.get('First Name').strip(), row.get('Last Name').strip())
                
                # Skip if both names are empty after cleaning
                if not name:
                    continue
                
                # Clean up the row data
                contact_data = {
                    k: v.strip() if isinstance(v, str) else v 
                    for k, v in row.items()
                    if v and str(v).strip()  # Only include non-empty values
                }
                
                # Add to contacts dictionary
                contacts[name] = contact_data
                
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        raise
    
    return contacts

def main():
    import argparse
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Parse contacts from a CSV file.')
    parser.add_argument('csv_file', help='Path to the CSV file containing contacts')
    args = parser.parse_args()
    
    # Get the absolute path of the input file
    csv_path = os.path.abspath(args.csv_file)
    
    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        return {}
    
    try:
        # Parse the contacts
        contacts = parse_contacts_to_dict(csv_path)
        
        # Print some stats
        print(f"Successfully parsed {len(contacts)} contacts")
        print("\nSample contacts:")
        
        # Print first 5 contacts as a sample
        for i, (key, data) in enumerate(contacts.items()):
            if i >= 5:  # Only show first 5
                break
            print(f"\nContact: {key}")
            for k, v in data.items():
                print(f"  {k}: {v}")
        
        return contacts
        
    except Exception as e:
        print(f"Error: {e}")
        return {}

if __name__ == "__main__":
    contacts = main()
