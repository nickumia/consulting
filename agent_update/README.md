# Agent Update

This tool updates agent information from HTML files and saves them as Excel (.xlsx) files. It's containerized with Docker for easy deployment.

## Prerequisites

- Docker
- (Optional) Python 3.7+ if running natively

## Usage with Docker (Recommended)

1. Build the Docker image:
   ```bash
   docker build -t agent_update .
   ```

2. Run the container to extract a table:
   ```bash
   docker run --rm -v "$(pwd):/app" agent_update input.html [output.xlsx]
   ```
   Replace `input.html` with your HTML file and `output.csv` with your desired output filename (optional).

## Native Python Usage

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:
   ```bash
python extract_table.py input.html [output.xlsx]
   ```

## Example

```bash
# Extract table from MyWFG.html and save as MyWFG.xlsx
docker run --rm -v "${PWD}:/app" agent_update "MyWFG - Associate Search--09272025.html" "MyWFG_Output.xlsx"
```

```bash
# For Windows Command Prompt
docker run --rm -v "%CD%:/app" agent_update pipeline old_agents.xlsx 'MyWFG - Associate Search--09272025.html' report.xlsx

# For Windows PowerShell
docker run --rm -v "${PWD}:/app" agent_update pipeline old_agents.xlsx 'MyWFG - Associate Search--09272025.html' report.xlsx
```

## Output

The script will create an Excel (.xlsx) file with the extracted table data. If no output filename is provided, it will use the input filename with a .xlsx extension.
