import requests
from bs4 import BeautifulSoup
import re

def debug_website_structure():
    """Debug the SIH website structure to understand how submission counts are displayed"""
    
    url = "https://sih.gov.in/sih2025PS"
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        print(f"🌐 Fetching: {url}")
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all tables
        tables = soup.find_all('table')
        print(f"📋 Found {len(tables)} tables")
        
        for i, table in enumerate(tables):
            print(f"\n🔍 TABLE {i+1}:")
            
            # Look for headers
            headers = []
            thead = table.find('thead')
            if thead:
                header_row = thead.find('tr')
                if header_row:
                    headers = [th.get_text().strip() for th in header_row.find_all(['th', 'td'])]
            else:
                # Look for first row with th elements
                for tr in table.find_all('tr'):
                    if tr.find('th'):
                        headers = [th.get_text().strip() for th in tr.find_all(['th', 'td'])]
                        break
            
            if headers:
                print("   Headers:", headers)
                
                # Look for PS Code and Submissions columns
                ps_idx = None
                sub_idx = None
                for j, header in enumerate(headers):
                    header_lower = header.lower()
                    if 'ps code' in header_lower or 'pscode' in header_lower:
                        ps_idx = j
                    elif 'submission' in header_lower:
                        sub_idx = j
                
                print(f"   PS Code column: {ps_idx}, Submissions column: {sub_idx}")
                
                # Show first few data rows
                tbody = table.find('tbody') or table
                rows = tbody.find_all('tr')
                data_rows = [row for row in rows if row.find('td')][:5]  # First 5 data rows
                
                print(f"   Sample data rows ({len(data_rows)} shown):")
                for row in data_rows:
                    cells = [td.get_text().strip() for td in row.find_all('td')]
                    if len(cells) >= max(ps_idx or 0, sub_idx or 0) + 1:
                        ps_code = cells[ps_idx] if ps_idx is not None else "N/A"
                        submission = cells[sub_idx] if sub_idx is not None else "N/A"
                        print(f"     PS: {ps_code}, Submissions: {submission}")
                    else:
                        print(f"     Row: {cells}")
            else:
                print("   No headers found")
                
                # Show first few rows anyway
                rows = table.find_all('tr')[:3]
                print("   Sample rows:")
                for row in rows:
                    cells = [td.get_text().strip() for td in row.find_all(['td', 'th'])]
                    print(f"     {cells}")
        
        # Also look for any divs or other structures that might contain submission counts
        print(f"\n🔍 Looking for other patterns...")
        
        # Search for text that looks like submission counts
        all_text = soup.get_text()
        submission_patterns = re.findall(r'submission[s]?\s*[:=]?\s*(\d+)', all_text, re.IGNORECASE)
        if submission_patterns:
            print(f"   Found submission patterns: {submission_patterns[:10]}")
        
        # Look for any elements with numbers that could be submission counts
        all_numbers = re.findall(r'\b\d{1,4}\b', all_text)
        number_counts = {}
        for num in all_numbers:
            number_counts[num] = number_counts.get(num, 0) + 1
        
        # Show most common numbers (might include submission counts)
        common_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"   Most common numbers: {common_numbers}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_website_structure()