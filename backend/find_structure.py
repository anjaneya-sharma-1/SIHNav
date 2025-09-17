import requests
from bs4 import BeautifulSoup

def find_table_structure():
    """Find the actual table structure and headers"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    url = "https://sih.gov.in/sih2025PS"
    
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find tables
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables")
        
        for i, table in enumerate(tables):
            print(f"\n=== TABLE {i+1} ===")
            
            # Look for header row
            header_row = None
            thead = table.find('thead')
            if thead:
                header_row = thead.find('tr')
                print("Found thead")
            else:
                # Look for first row with th elements
                for tr in table.find_all('tr')[:3]:
                    if tr.find('th'):
                        header_row = tr
                        print("Found th row")
                        break
            
            if header_row:
                headers = header_row.find_all(['th', 'td'])
                print(f"Headers ({len(headers)} columns):")
                for j, header in enumerate(headers):
                    text = ' '.join(header.get_text().strip().split())
                    print(f"  {j}: '{text}'")
            else:
                print("No header row found")
                
            # Show first few data rows
            tbody = table.find('tbody') or table
            rows = tbody.find_all('tr')
            data_rows = [row for row in rows if row.find('td')]
            
            print(f"Data rows: {len(data_rows)}")
            
            if data_rows:
                print("First data row:")
                first_row = data_rows[0]
                tds = first_row.find_all('td')
                for j, td in enumerate(tds):
                    text = ' '.join(td.get_text().strip().split())[:80]
                    print(f"  {j}: '{text}'")
                    
                if len(data_rows) > 1:
                    print("Second data row:")
                    second_row = data_rows[1]
                    tds = second_row.find_all('td')
                    for j, td in enumerate(tds):
                        text = ' '.join(td.get_text().strip().split())[:80]
                        print(f"  {j}: '{text}'")
            
            # Only show first table with data
            if data_rows:
                break
        
        # Search for any text that might contain submission counts
        print("\n=== SEARCHING FOR 'SUBMISSION' KEYWORDS ===")
        page_text = soup.get_text().lower()
        if 'submission' in page_text:
            print("Found 'submission' in page text")
            
            # Look for numbers near submission
            lines = soup.get_text().split('\n')
            for line in lines:
                if 'submission' in line.lower() and any(char.isdigit() for char in line):
                    print(f"Line with submission and numbers: {line.strip()}")
        else:
            print("No 'submission' text found on page")
            
        # Check if this might be a dynamic page
        scripts = soup.find_all('script')
        print(f"\nFound {len(scripts)} script tags")
        for script in scripts[:3]:
            if script.string and ('ajax' in script.string.lower() or 'fetch' in script.string.lower()):
                print("Found AJAX/fetch in script - might be dynamic content")
                break
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_table_structure()