import pandas as pd
import re

def is_valid_name_part(part):
    """Check if a part of a name is valid (not an abbreviation or code)."""
    # Common invalid patterns (add more as needed)
    invalid_patterns = [
        r'^[A-Z0-9]{1,3}$',  # 1-3 uppercase letters/numbers (e.g., Ch, CF, A1)
        r'^[a-z]$',           # Single lowercase letter
        r'^[A-Z]\.?$',       # Single uppercase letter, optionally followed by a dot
        r'^[^A-Za-z]',        # Starts with non-letter
        r'[0-9]',             # Contains numbers
    ]
    
    part = str(part).strip()
    if not part:
        return False
    
    # Check against all invalid patterns
    for pattern in invalid_patterns:
        if re.search(pattern, part, re.IGNORECASE):
            return False
    return True

def clean_name(name):
    """Clean and split a full name into first and last name."""
    if pd.isna(name) or not str(name).strip():
        return pd.Series({'First Name': '', 'Last Name': ''})
    
    # Clean and normalize the name
    name = str(name).strip()
    
    # Remove content in parentheses, brackets, etc.
    name = re.sub(r'\s*[\[\(].*?[\]\)]\s*', ' ', name)
    
    # Remove special characters but keep accented characters and hyphens
    name = re.sub(r'[^\w\s-]', ' ', name, flags=re.UNICODE)
    
    # Split and filter out invalid parts
    parts = [p for p in name.split() if is_valid_name_part(p)]
    
    # Handle different name formats
    if not parts:
        return pd.Series({'First Name': '', 'Last Name': ''})
    elif len(parts) == 1:
        return pd.Series({'First Name': parts[0], 'Last Name': ''})
    else:
        # If we have at least 2 parts, last part is last name, rest is first name
        return pd.Series({
            'First Name': ' '.join(parts[:-1]),
            'Last Name': parts[-1]
        })

def try_read_csv(file_path):
    """Try reading CSV with different encodings."""
    encodings = ['utf-8', 'latin-1', 'utf-16', 'cp1252']
    
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding, on_bad_lines='warn')
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error with {encoding}: {str(e)}")
            continue
    
    raise ValueError(f"Failed to read {file_path} with any of the attempted encodings")

def main():
    input_file = 'contacts Phone-original.csv'
    output_file = 'contacts_cleaned.csv'
    
    try:
        # Read the CSV file with different encoding attempts
        print(f"Attempting to read {input_file}...")
        df = try_read_csv(input_file)
        
        # Find name columns (case insensitive)
        name_columns = [col for col in df.columns if 'name' in col.lower()]
        
        if not name_columns:
            print("No name columns found in the CSV.")
            return
            
        # Process each name column
        for col in name_columns:
            # Clean and split names
            df[[f"{col}_temp_first", f"{col}_temp_last"]] = df[col].apply(clean_name)
            
            # Replace original column with cleaned first name
            df[col] = df[f"{col}_temp_first"]
            
            # Create or update Last Name column
            last_name_col = f"{col}_Last" if "First" in col else f"Last Name"
            df[last_name_col] = df[f"{col}_temp_last"]
            
            # Remove temporary columns
            df = df.drop(columns=[f"{col}_temp_first", f"{col}_temp_last"])
        
        # Save to new CSV
        df.to_csv(output_file, index=False)
        print(f"Successfully cleaned and saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
