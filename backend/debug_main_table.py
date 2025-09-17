import requests
from bs4 import BeautifulSoup
import re

def debug_main_listing():
    """Debug the main listing table structure"""
    
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
        
        # Look for the main listing table - it should be the first/largest table
        tables = soup.find_all('table')
        print(f"📋 Found {len(tables)} tables total")
        
        # Check first few tables for the main listing
        for i, table in enumerate(tables[:5]):
            print(f"\n🔍 MAIN TABLE {i+1}:")
            
            # Count rows to identify the main listing table
            rows = table.find_all('tr')
            print(f"   Total rows: {len(rows)}")
            
            if len(rows) < 10:  # Skip small tables
                print("   ⏭️  Skipping small table")
                continue
            
            # Look for headers in first row
            if rows:
                first_row = rows[0]
                headers = [cell.get_text().strip() for cell in first_row.find_all(['th', 'td'])]
                print(f"   Headers: {headers}")
                
                # Check if this looks like the main listing
                header_text = ' '.join(headers).lower()
                if any(keyword in header_text for keyword in ['ps code', 'submission', 'organization', 'title']):
                    print("   ✅ This looks like the main listing table!")
                    
                    # Show sample rows
                    print("   📄 Sample data rows:")
                    for j, row in enumerate(rows[1:6]):  # Skip header, show next 5
                        cells = [cell.get_text().strip() for cell in row.find_all('td')]
                        if cells:
                            print(f"     Row {j+1}: {cells}")
                    
                    # Try to identify column positions
                    ps_idx = None
                    sub_idx = None
                    org_idx = None
                    title_idx = None
                    
                    for k, header in enumerate(headers):
                        h_lower = header.lower()
                        if 'ps code' in h_lower or 'ps id' in h_lower:
                            ps_idx = k
                        elif 'submission' in h_lower:
                            sub_idx = k
                        elif 'organization' in h_lower:
                            org_idx = k
                        elif 'title' in h_lower:
                            title_idx = k
                    
                    print(f"   🎯 Column indices - PS: {ps_idx}, Submissions: {sub_idx}, Org: {org_idx}, Title: {title_idx}")
                    
                    return  # Found the main table, stop here
                else:
                    print("   ❌ Doesn't look like main listing")
        
        # If no main table found, look for patterns in the page
        print(f"\n🔍 Looking for submission count patterns in page text...")
        page_text = soup.get_text()
        
        # Look for "submission" followed by numbers
        submission_matches = re.findall(r'submission[s]?\s*[:=]?\s*(\d+)', page_text, re.IGNORECASE)
        if submission_matches:
            print(f"   Found submission patterns: {submission_matches[:20]}")
        
        # Look for PS codes with numbers
        ps_matches = re.findall(r'(SIH\d+|PS\d+|\d{5})', page_text)
        if ps_matches:
            print(f"   Found PS code patterns: {ps_matches[:20]}")
        
        # Check if submission counts might be loaded via JavaScript/AJAX
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and ('submission' in script.string.lower() or 'ajax' in script.string.lower()):
                print(f"   📜 Found relevant script: {script.string[:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_main_listing()