import requests
from bs4 import BeautifulSoup
import re

def debug_submission_extraction():
    """Debug submission count extraction"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    url = "https://sih.gov.in/sih2025PS"
    
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all table rows
        rows = soup.find_all('tr')
        print(f"Found {len(rows)} total rows")
        
        # Look for rows with data
        data_rows = 0
        for i, row in enumerate(rows[:20]):  # Check first 20 rows
            tds = row.find_all('td')
            if len(tds) >= 6:
                data_rows += 1
                print(f"\nRow {i} has {len(tds)} columns:")
                for j, td in enumerate(tds[:7]):  # Show first 7 columns
                    text = ' '.join(td.get_text().strip().split())[:50]
                    print(f"  Col {j}: {text}")
                
                # Special focus on PS Code and Submission columns
                if len(tds) > 4:
                    ps_code = ' '.join(tds[4].get_text().strip().split())
                    print(f"  PS Code (col 4): '{ps_code}'")
                
                if len(tds) > 5:
                    submission = ' '.join(tds[5].get_text().strip().split())
                    print(f"  Submission (col 5): '{submission}'")
                    
                    # Try to convert to int
                    try:
                        sub_int = int(submission)
                        print(f"  Submission as int: {sub_int}")
                    except:
                        print(f"  Submission conversion failed: '{submission}'")
                
                if data_rows >= 5:  # Only show first 5 data rows
                    break
        
        print(f"\nTotal data rows found: {data_rows}")
        
        # Also check if there are any rows with submission counts > 0
        print("\nLooking for rows with non-zero submissions...")
        found_nonzero = 0
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 6:
                try:
                    submission_text = ' '.join(tds[5].get_text().strip().split())
                    submission_count = int(submission_text)
                    if submission_count > 0:
                        found_nonzero += 1
                        ps_code = ' '.join(tds[4].get_text().strip().split())
                        print(f"  PS {ps_code}: {submission_count} submissions")
                        
                        if found_nonzero >= 10:  # Show first 10
                            break
                except:
                    continue
        
        if found_nonzero == 0:
            print("  No rows with submission count > 0 found!")
        else:
            print(f"  Found {found_nonzero} rows with submissions > 0")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_submission_extraction()