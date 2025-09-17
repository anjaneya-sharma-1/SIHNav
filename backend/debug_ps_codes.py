import requests
from bs4 import BeautifulSoup
import re

def debug_ps_codes():
    """Debug what PS codes are actually found"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    url = "https://sih.gov.in/sih2025PS"
    
    def extract_numeric_ps_id(value):
        if not value:
            return None
        match = re.search(r'(\d{3,})', str(value))
        if not match:
            return None
        try:
            return int(match.group(1))
        except Exception:
            return None
    
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main table
        tables = soup.find_all('table')
        main_table = None
        
        for table in tables:
            tbody = table.find('tbody') or table
            rows = tbody.find_all('tr')
            data_rows = [row for row in rows if row.find('td')]
            if len(data_rows) > 100:  # Main table should have many rows
                main_table = table
                break
        
        if not main_table:
            print("Could not find main table")
            return
        
        print("=== ANALYZING MAIN TABLE ===")
        
        # Check header
        header_row = main_table.find('thead')
        if header_row:
            header_row = header_row.find('tr')
        else:
            header_row = main_table.find('tr')
        
        if header_row:
            headers = header_row.find_all(['th', 'td'])
            print("Headers:")
            for i, header in enumerate(headers):
                text = ' '.join(header.get_text().strip().split())
                print(f"  {i}: '{text}'")
        
        # Check first few rows to understand structure
        tbody = main_table.find('tbody') or main_table
        rows = tbody.find_all('tr')
        data_rows = [row for row in rows if row.find('td')]
        
        print(f"\nAnalyzing first 5 data rows from {len(data_rows)} total rows:")
        
        for i, row in enumerate(data_rows[:5]):
            tds = row.find_all('td')
            print(f"\nRow {i+1} ({len(tds)} columns):")
            
            # Look for PS codes in each column
            for j, td in enumerate(tds):
                text = ' '.join(td.get_text().strip().split())
                if len(text) > 100:
                    text = text[:100] + "..."
                
                # Check if this looks like a PS ID
                if re.search(r'\b(SIH)?25\d{3}\b', text):
                    print(f"  {j}: '{text}' ← LOOKS LIKE PS ID!")
                elif re.search(r'\b\d{4,}\b', text):
                    print(f"  {j}: '{text}' ← HAS NUMBERS")
                else:
                    print(f"  {j}: '{text}'")
        
        # Search specifically for SIH25001 pattern
        print(f"\n=== SEARCHING FOR SIH25XXX PATTERN ===")
        page_text = soup.get_text()
        sih_matches = re.findall(r'SIH25\d{3}', page_text)
        if sih_matches:
            unique_matches = list(set(sih_matches))
            print(f"Found {len(unique_matches)} unique SIH25XXX codes:")
            for match in sorted(unique_matches)[:10]:
                print(f"  {match}")
        else:
            print("No SIH25XXX codes found in page text")
            
        # Look for 25001 style numbers
        plain_matches = re.findall(r'\b25\d{3}\b', page_text)
        if plain_matches:
            unique_plain = list(set(plain_matches))
            print(f"Found {len(unique_plain)} plain 25XXX codes:")
            for match in sorted(unique_plain)[:10]:
                print(f"  {match}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_ps_codes()