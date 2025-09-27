# HTML Table Extractor

This tool extracts tables from HTML files and saves them as CSV files. It's containerized with Docker for easy deployment.

## Prerequisites

- Docker
- (Optional) Python 3.7+ if running natively

## Usage with Docker (Recommended)

1. Build the Docker image:
   ```bash
   docker build -t html-table-extractor .
   ```

2. Run the container to extract a table:
   ```bash
   docker run --rm -v "$(pwd):/app" html-table-extractor input.html [output.csv]
   ```
   Replace `input.html` with your HTML file and `output.csv` with your desired output filename (optional).

## Native Python Usage

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:
   ```bash
   python extract_table.py input.html [output.csv]
   ```

## Example

```bash
# Extract table from MyWFG.html and save as MyWFG.csv
docker run --rm -v "$(pwd):/app" html-table-extractor "MyWFG - Associate Search--09272025.html" "MyWFG_Output.csv"
```

## Output

The script will create a CSV file with the extracted table data. If no output filename is provided, it will use the input filename with a .csv extension.
