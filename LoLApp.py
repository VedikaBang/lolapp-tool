import requests
import yaml
import re
from bs4 import BeautifulSoup
import json
import logging
from tabulate import tabulate
import markdown as md

# Set up basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def clean_html_tags(text):
    """
    Remove HTML tags from the text and preserve new lines.
    
    :param text: A string containing HTML.
    :return: A string with HTML tags removed and new lines preserved.
    """
    # Replace HTML new line tags with newline characters
    text = text.replace('<br>', '\n').replace('<br/>', '\n').replace('</p>', '\n')
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Reduce multiple newlines to a single newline
    clean_text = re.sub(r'\n\s*\n', '\n', clean_text)
    return clean_text.strip()

def get_apps():
    """
    Scrape the specified webpage for applications and their URLs.
    
    :return: A dictionary with app names as keys and URLs as values.
    """
    apps = {}
    try:
        response = requests.get("https://vedikabang.github.io/LoLApp/")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        table_body = soup.find('tbody', id='tableListBody')
        if table_body:
            for row in table_body.find_all('tr'):
                app_cell = row.find('td')
                if app_cell and app_cell.find('a'):
                    app_name = app_cell.text.strip()
                    app_url = app_cell.find('a')['href'].strip()
                    apps[app_name] = app_url.split('/')[-2]
        else:
            logging.warning("No table body found on the page.")
    except requests.RequestException as e:
        logging.error(f"Error fetching applications: {e}")
    return apps


def fetch_detection_rule_links(app_name):
    """
    Generate detection rule links for a given application.
    
    :param app_name: Name of the application.
    :return: A list of URLs for the detection rules.
    """
    rule_links = []
    for i in range(5):  # Assuming 5 rules per app
        url = (f"https://raw.githubusercontent.com/VedikaBang/LoLApp/main/"
               f"detection_rules/{app_name}/{i}.yaml")
        rule_links.append(url)
    return rule_links
    
def process_markdown_table(markdown_table):
    """
    Convert markdown table content to a structured list of dictionaries,
    preserving the structure and new lines.
    
    :param markdown_table: A string containing markdown table syntax.
    :return: A list of dictionaries with each dictionary representing a row.
    """
    # Splitting rows on new lines and columns on the pipe character
    rows = [row.strip().split('|')[1:-1] for row in
            markdown_table.strip().split('\n') if row.strip()]

    # The first row is the header
    headers = rows.pop(0)
    headers = [header.strip() for header in headers]

    # Process the body rows, ignoring separator lines
    body_rows = [row for row in rows if not set(cell.strip() for cell in row) == {'---'}]

    # Create a list of dictionaries for each row
    structured_rows = [dict(zip(headers, [clean_html_tags(cell) for cell in row]))
                       for row in body_rows]

    return structured_rows

def process_markdown_content(markdown_content, app_name):
    """
    Process markdown content to extract and structure 'App Artifacts' and 
    'MITRE ATT&CK References' sections.

    :param markdown_content: A string containing markdown syntax.
    :param app_name: Name of the application.
    :return: A dictionary with extracted and structured data.
    """
    data = {'Sigma Rule Links': fetch_detection_rule_links(app_name)}

    # Process App Artifacts section
    app_artifacts_section = re.search(r'## App Artifacts\s*(.*?)##', markdown_content, re.DOTALL)
    if app_artifacts_section:
        markdown_table = app_artifacts_section.group(1)
        artifacts_table = process_markdown_table(markdown_table)
        data['App Artifacts'] = artifacts_table  # This will be a list of dictionaries

    # The rest of the function remains unchanged...

    return data

import requests
import yaml
import re
from bs4 import BeautifulSoup
import json
import logging
from tabulate import tabulate
import markdown as md

# Set up basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def clean_html_tags(text):
    """
    Remove HTML tags from the text and preserve new lines.
    
    :param text: A string containing HTML.
    :return: A string with HTML tags removed and new lines preserved.
    """
    # Replace HTML new line tags with newline characters
    text = text.replace('<br>', '\n').replace('<br/>', '\n').replace('</p>', '\n')
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Reduce multiple newlines to a single newline
    clean_text = re.sub(r'\n\s*\n', '\n', clean_text)
    return clean_text.strip()

def get_apps():
    """
    Scrape the specified webpage for applications and their URLs.
    
    :return: A dictionary with app names as keys and URLs as values.
    """
    apps = {}
    try:
        response = requests.get("https://vedikabang.github.io/LoLApp/")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        table_body = soup.find('tbody', id='tableListBody')
        if table_body:
            for row in table_body.find_all('tr'):
                app_cell = row.find('td')
                if app_cell and app_cell.find('a'):
                    app_name = app_cell.text.strip()
                    app_url = app_cell.find('a')['href'].strip()
                    apps[app_name] = app_url.split('/')[-2]
        else:
            logging.warning("No table body found on the page.")
    except requests.RequestException as e:
        logging.error(f"Error fetching applications: {e}")
    return apps


def fetch_detection_rule_links(app_name):
    """
    Generate detection rule links for a given application.
    
    :param app_name: Name of the application.
    :return: A list of URLs for the detection rules.
    """
    rule_links = []
    for i in range(5):  # Assuming 5 rules per app
        url = (f"https://raw.githubusercontent.com/VedikaBang/LoLApp/main/"
               f"detection_rules/{app_name}/{i}.yaml")
        rule_links.append(url)
    return rule_links
    
def process_markdown_table(markdown_table):
    """
    Convert markdown table content to a structured list of dictionaries,
    preserving the structure and new lines.
    
    :param markdown_table: A string containing markdown table syntax.
    :return: A list of dictionaries with each dictionary representing a row.
    """
    # Splitting rows on new lines and columns on the pipe character
    rows = [row.strip().split('|')[1:-1] for row in
            markdown_table.strip().split('\n') if row.strip()]

    # The first row is the header
    headers = rows.pop(0)
    headers = [header.strip() for header in headers]

    # Process the body rows, ignoring separator lines
    body_rows = [row for row in rows if not set(cell.strip() for cell in row) == {'---'}]

    # Create a list of dictionaries for each row
    structured_rows = [dict(zip(headers, [clean_html_tags(cell) for cell in row]))
                       for row in body_rows]

    return structured_rows

def process_markdown_content(markdown_content, app_name):
    """
    Process markdown content to extract and structure 'App Artifacts' and 
    'MITRE ATT&CK References' sections.

    :param markdown_content: A string containing markdown syntax.
    :param app_name: Name of the application.
    :return: A dictionary with extracted and structured data.
    """
    data = {'Sigma Rule Links': fetch_detection_rule_links(app_name)}

    # Process App Artifacts section
    app_artifacts_section = re.search(r'## App Artifacts\s*(.*?)##', markdown_content, re.DOTALL)
    if app_artifacts_section:
        markdown_table = app_artifacts_section.group(1)
        artifacts_table = process_markdown_table(markdown_table)
        data['App Artifacts'] = artifacts_table  # This will be a list of dictionaries

    # The rest of the function remains unchanged...

    return data



def LoLApp(app_name: str):
    # Retrieve applications from the webpage
    apps = get_apps()
    
    # Find the URL for the given application name, case-insensitive
    app_url = next((url for name, url in apps.items() if name.lower() == app_name.lower()), None)

    if app_url:
        # Dictionary to store app data
        app_data = {}
        app_path = apps[app_name]
        # Construct the URL for the markdown content
        markdown_url = (f"https://raw.githubusercontent.com/VedikaBang/LoLApp/main/"
                        f"lolapp_site/content/{app_path}.md")

        try:
            # Fetch the markdown content from the URL
            response = requests.get(markdown_url)
            if response.status_code == 200:
                content = response.text
                # Split the content into YAML front matter and markdown body
                parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
                yaml_content, markdown_body = parts[1], parts[2]
                # Parse the YAML front matter
                metadata = yaml.safe_load(yaml_content)
                # Store title and tags
                app_data['Title'] = metadata.get('title')
                app_data['Tags'] = metadata.get('tags', [])
                # Process the markdown content
                app_data.update(process_markdown_content(markdown_body, app_path))

                # Save the extracted data to a JSON file
                with open(f"{app_name}_data.json", "w") as json_file:
                    json.dump(app_data, json_file, indent=4)

                logging.info(f"Data for {app_name} saved to JSON file.")
            else:
                # Log an error if the markdown content cannot be fetched
                logging.error(f"Error fetching markdown for {app_name}: HTTP {response.status_code}")
        except Exception as e:
            # Log any exceptions that occur during processing
            logging.error(f"An error occurred: {e}")
    else:
        # Log a warning if the application is not found
        logging.warning(f"App not found on LoLApps: {app_name}")


