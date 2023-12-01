import requests
import yaml
import re
from bs4 import BeautifulSoup
from utils import colors
from tabulate import tabulate
import json

def clean_html_tags(text):
    """ Remove HTML tags from the text """
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text


def get_apps():
    apps = dict()
    try:
        r = requests.get("https://vedikabang.github.io/LoLApp/")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        # Find the table body
        table_body = soup.find('tbody', id='tableListBody')
        if table_body:
            # Iterate over each table row
            for row in table_body.find_all('tr'):
                # Extract the first 'td' element which contains the application link
                app_cell = row.find('td')
                if app_cell and app_cell.find('a'):
                    app_name = app_cell.text.strip()
                    app_url = app_cell.find('a')['href'].strip()
                    # Store only the relative path segment (e.g., 'anydesk')
                    apps[app_name] = app_url.split('/')[-2]
        else:
            print("No table body found on the page.")

    except requests.RequestException as e:
        print(f"Error fetching applications: {e}")
    print("Fetched Apps:", apps)
    return apps



def process_markdown_table(markdown_table):
    """Convert markdown table content to a list of lists and print using tabulate."""
    rows = [row.strip().split('|')[1:-1] for row in markdown_table.strip().split('\n') if row.strip()]
    header = rows.pop(0)  # The first row is the header
    # Clean the HTML tags from each cell and remove markdown artifacts like '---'
    clean_rows = [[clean_html_tags(cell) for cell in row] for row in rows if not set(cell.strip() for cell in row) == {'---'}]
    
    print(tabulate(clean_rows, headers=header, tablefmt='fancy_grid'))



def process_markdown_content(markdown_content):
    markdown_tables = re.findall(r'(\|(?:[^\n]*\|)+\n\|(?:\s*\:?\-+\:?\s*\|)+\n(?:\|(?:[^\n]*\|)+\n)+)', markdown_content, re.MULTILINE)
    
    for table in markdown_tables:
        process_markdown_table(table)

    app_artifacts_section = re.search(r'## App Artifacts\s*(.*?)##', markdown_content, re.DOTALL)
    if app_artifacts_section:
        print(colors("App Artifacts:", 93))
        print(app_artifacts_section.group(1))

    TTPs_Section = re.search(r'## MITRE ATT&CK References\s*(.*?)##', markdown_content, re.DOTALL)
    if TTPs_Section:
        print(colors("MITRE ATT&CK References:", 93))
        print(TTPs_Section.group(1))

    rules_section = re.search(r'## Rules\s*(.*?)##', markdown_content, re.DOTALL)
    if rules_section:
        print(colors("Sigma Rules:", 93))
        print(rules_section.group(1))



def LoLApp(app_name: str):
    apps = get_apps()
    app_url = next((url for name, url in apps.items() if name.lower() == app_name.lower()), None)

    if app_url:
        app_data = {}  # Dictionary to store app data
        app_path = apps[app_name]  # Get the path corresponding to the app name
        markdown_url = f"https://raw.githubusercontent.com/VedikaBang/LoLApp/main/lolapp_site/content/{app_path}.md"
        print("Attempting to fetch:", markdown_url)

        if not markdown_url.endswith('.md'):
            markdown_url += '.md'
        try:
            response = requests.get(markdown_url)
            if response.status_code == 200:
                content = response.text
                parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
                yaml_content, markdown_body = parts[1], parts[2]
                metadata = yaml.safe_load(yaml_content)
                app_data['Title'] = metadata.get('title')
                app_data['Tags'] = metadata.get('tags', [])

                # Here, you should process the markdown_body and add the relevant data to app_data
                # For example, if process_markdown_content returns a dictionary:
                # app_data.update(process_markdown_content(markdown_body))

                # Save to JSON file
                with open(f"{app_name}_data.json", "w") as json_file:
                    json.dump(app_data, json_file, indent=4)

                print(f"Data for {app_name} saved to JSON file.")
            else:
                print(colors(f"[!] Error fetching markdown for {app_name}: HTTP {response.status_code}", 91))
        except Exception as e:
            print(colors(f"[!] An error occurred: {e}", 91))
    else:
        print(colors("[!] App not found on LoLApps: ", 91))
