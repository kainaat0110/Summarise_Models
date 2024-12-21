import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3
from datetime import datetime

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_notes_link(url, keyword):
    try:
        # Send an HTTP request to the URL with SSL verification disabled
        response = requests.get(url, verify=False)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links on the page
        links = soup.find_all('a', href=True)

        latest_resources = {}  # Dictionary to track latest data per department

        # Search for the keyword in link text
        for link in links:
            if keyword.lower() in link.get_text().lower():
                full_url = urljoin(url, link['href'])
                print(f"Checking link for '{keyword}': {full_url}")
                
                # Fetch the resource page
                page_response = requests.get(full_url, verify=False)
                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.text, 'html.parser')

                    # Extract teacher's name, department, and date
                    teacher_name = extract_teacher_name(page_soup)
                    department = extract_department(page_soup)
                    upload_date = extract_upload_date(page_soup)

                    # Ensure valid date before processing
                    if upload_date:
                        if department not in latest_resources or upload_date > latest_resources[department]['date']:
                            # Store latest resource for each department
                            latest_resources[department] = {
                                'url': full_url,
                                'teacher': teacher_name,
                                'date': upload_date
                            }

        # Print the latest resources for each department
        if latest_resources:
            for dept, resource in latest_resources.items():
                print(f"Department: {dept}")
                print(f"Teacher: {resource['teacher']}")
                print(f"Date: {resource['date']}")
                print(f"Link: {resource['url']}")
        else:
            print(f"No latest resources found for keyword: '{keyword}'")

        return latest_resources

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_teacher_name(soup):
    """Extract teacher's name from the page soup."""
    # Example: Adjust according to actual HTML structure
    teacher_tag = soup.find('p', class_='teacher-name')  # Replace with actual tag/identifier
    if teacher_tag:
        return teacher_tag.get_text(strip=True)
    return "Unknown Teacher"

def extract_department(soup):
    """Extract department from the page soup."""
    # Example: Adjust according to actual HTML structure
    dept_tag = soup.find('p', class_='department-name')  # Replace with actual tag/identifier
    if dept_tag:
        return dept_tag.get_text(strip=True)
    return "Unknown Department"

def extract_upload_date(soup):
    """Extract upload date from the page soup."""
    date_formats = ["%d %B %Y", "%d-%m-%Y"]  # Update based on expected formats
    # Example: Adjust according to actual HTML structure
    date_tag = soup.find('span', class_='upload-date')  # Replace with actual tag/identifier
    if date_tag:
        date_text = date_tag.get_text(strip=True)
        for date_format in date_formats:
            try:
                return datetime.strptime(date_text, date_format)
            except ValueError:
                continue
    return None

# Starting URL
start_url = 'https://dbit.in/'  # Update with the correct URL for the site you're scraping

# Take input from the user
keyword = input("Enter the topic you want to find (e.g., 'heap sort'): ")

# Start searching
result = find_notes_link(start_url, keyword)

if result:
    print(f"Results found for keyword: {keyword}")
else:
    print("No results found.")
