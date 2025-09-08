import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from typing import List, Dict, Optional

class SIHScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def scrape_sih_problems(self, url: str, start_ps_id: Optional[str] = None, incremental: bool = False) -> List[Dict]:
        """
        Scrape all problem statements from SIH website
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all modal divs that contain problem statements
            problem_modals = soup.find_all('div', {'id': re.compile(r'ViewProblemStatement\d+')})
            
            print(f"Found {len(problem_modals)} problem statement modals")
            
            problems = []
            for modal in problem_modals:
                try:
                    table_row = modal.find_parent('tr') if modal else None
                    problem_data = self.extract_problem_data(modal, table_row=table_row)
                    if problem_data:
                        problems.append(problem_data)
                        print(f"✓ Extracted: {problem_data['ps_id']} - {problem_data['title'][:50]}...")
                except Exception as e:
                    print(f"✗ Error extracting problem: {e}")
                    continue
            
            return problems
            
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return []

    def extract_problem_data(self, modal_div, table_row=None) -> Optional[Dict]:
        """
        Extract problem data from a single modal div and its parent table row
        
        Args:
            modal_div: The modal div containing detailed problem info
            table_row: The parent table row containing submission count and other summary data
        """
        try:
            # Find the table containing all the data
            table = modal_div.find('table', {'id': 'settings'})
            if not table:
                return None
            
            # Find all rows
            rows = table.find_all('tr')
            if len(rows) < 7:  # Should have at least 7 rows for all required fields
                return None
            
            # Extract data using the pattern you identified
            problem_data = {}
            
            # Method 1: Extract using style-2 divs (for PS ID, Title, Description)
            style_2_divs = table.find_all('div', class_='style-2')
            
            if len(style_2_divs) >= 3:
                # PS ID (first style-2 div)
                problem_data['ps_id'] = self.clean_text(style_2_divs[0].get_text())
                
                # Title (second style-2 div)
                problem_data['title'] = self.clean_text(style_2_divs[1].get_text())
                
                # Description (third style-2 div)
                problem_data['description'] = self.clean_html_text(style_2_divs[2])
            
            # Method 2: Extract other fields from table rows
            for row in rows:
                th = row.find('th')
                td = row.find('td')
                
                if th and td:
                    field_name = self.clean_text(th.get_text()).lower()
                    field_value = self.clean_text(td.get_text())
                    
                    # Map fields to our desired keys
                    if 'organization' in field_name:
                        problem_data['organization'] = field_value
                    elif 'department' in field_name:
                        problem_data['department'] = field_value
                    elif 'category' in field_name:
                        problem_data['category'] = field_value
                    elif 'theme' in field_name:
                        problem_data['theme'] = field_value
                    elif 'youtube' in field_name:
                        # Extract YouTube link if present
                        link = td.find('a')
                        problem_data['youtube_link'] = link.get('href') if link else ''
                    elif 'dataset' in field_name:
                        # Extract dataset links if present
                        links = td.find_all('a')
                        problem_data['dataset_links'] = [link.get('href') for link in links if link.get('href')]
                    elif 'contact' in field_name:
                        # Extract contact info if present
                        link = td.find('a')
                        problem_data['contact_info'] = link.get('href') if link else ''
            
            # Method 3: Extract data from parent table row (submission count, etc.)
            if table_row:
                self.extract_row_data(table_row, problem_data)
            
            # Validate that we have the essential fields
            required_fields = ['ps_id', 'title', 'description']
            if not all(field in problem_data for field in required_fields):
                print(f"Missing required fields in problem data: {problem_data}")
                return None
            
            # Add metadata
            problem_data['scraped_at'] = time.time()
            problem_data['scraped_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            return problem_data
            
        except Exception as e:
            print(f"Error extracting problem data: {e}")
            return None
    
    def extract_row_data(self, table_row, problem_data: Dict):
        """
        Extract additional data from the table row containing the modal
        Based on the structure: Serial | Organization | Title+Modal | Category | PS Code | Submissions | Theme
        """
        try:
            tds = table_row.find_all('td')
            if len(tds) >= 6:  # Should have at least 6 columns
                # Column positions based on your HTML structure:
                # 0: Serial number
                # 1: Organization (backup, already extracted from modal)
                # 2: Title with modal link (backup, already extracted from modal)  
                # 3: Category (backup, already extracted from modal)
                # 4: PS Code (like SIH25001)
                # 5: Submission count
                # 6: Theme (backup, already extracted from modal)
                
                # Extract PS Code (column 4)
                if len(tds) > 4:
                    ps_code = self.clean_text(tds[4].get_text())
                    if ps_code:
                        problem_data['ps_code'] = ps_code
                
                # Extract Submission Count (column 5)
                if len(tds) > 5:
                    submission_count = self.clean_text(tds[5].get_text())
                    try:
                        problem_data['submission_count'] = int(submission_count)
                    except (ValueError, TypeError):
                        problem_data['submission_count'] = 0
                
                # Use row data as backup for missing modal data
                if 'organization' not in problem_data and len(tds) > 1:
                    org = self.clean_text(tds[1].get_text())
                    if org:
                        problem_data['organization'] = org
                
                if 'category' not in problem_data and len(tds) > 3:
                    category = self.clean_text(tds[3].get_text())
                    if category:
                        problem_data['category'] = category
                
                if 'theme' not in problem_data and len(tds) > 6:
                    theme = self.clean_text(tds[6].get_text())
                    if theme:
                        problem_data['theme'] = theme
                        
        except Exception as e:
            print(f"Warning: Error extracting row data: {e}")
            # Don't fail the whole extraction for row data errors
            pass
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        cleaned = ' '.join(text.strip().split())
        return cleaned
    
    def clean_html_text(self, element) -> str:
        """Clean HTML text while preserving some formatting"""
        if not element:
            return ""
        
        # Get HTML content
        html_content = str(element)
        
        # Replace HTML breaks with newlines
        html_content = re.sub(r'<br\s*/?>', '\n', html_content)
        
        # Remove HTML tags but keep the text
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        
        # Clean up multiple newlines
        text = re.sub(r'\n+', '\n\n', text)
        
        return text.strip()
    
    def save_to_json(self, problems: List[Dict], filename: str = 'sih_problems.json', merge_existing: bool = False):
        """Save problems to JSON file, optionally merging with existing by ps_id."""
        try:
            output: List[Dict] = problems or []
            if merge_existing and os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        existing = json.load(f)
                    if not isinstance(existing, list):
                        existing = []
                except Exception:
                    existing = []

                # Merge by ps_id when available
                items_without_id = [p for p in existing if isinstance(p, dict) and not p.get('ps_id')]
                by_id: Dict[str, Dict] = {p.get('ps_id'): p for p in existing if isinstance(p, dict) and p.get('ps_id')}
                for p in output:
                    if isinstance(p, dict) and p.get('ps_id'):
                        by_id[p['ps_id']] = p
                    else:
                        items_without_id.append(p)
                output = items_without_id + list(by_id.values())

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved {len(output)} problems to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def save_to_csv(self, problems: List[Dict], filename: str = 'sih_problems.csv', merge_existing: bool = False):
        """Save problems to CSV file, optionally merging with existing by ps_id."""
        try:
            import pandas as pd

            df_new = pd.DataFrame(problems)
            if merge_existing and os.path.exists(filename):
                try:
                    df_existing = pd.read_csv(filename)
                except Exception:
                    df_existing = pd.DataFrame()
                if not df_existing.empty:
                    combined = pd.concat([df_existing, df_new], ignore_index=True)
                else:
                    combined = df_new
                if 'ps_id' in combined.columns:
                    combined = combined.drop_duplicates(subset=['ps_id'], keep='last')
                else:
                    combined = combined.drop_duplicates(keep='last')
                combined.to_csv(filename, index=False, encoding='utf-8')
                print(f"✓ Saved {len(combined)} problems to {filename}")
            else:
                df_new.to_csv(filename, index=False, encoding='utf-8')
                print(f"✓ Saved {len(df_new)} problems to {filename}")
        except ImportError:
            # Fallback to csv module
            try:
                import csv
                fieldnames = sorted({k for p in problems for k in (p.keys() if isinstance(p, dict) else [])})
                file_exists = os.path.exists(filename)
                mode = 'a' if merge_existing and file_exists else 'w'
                with open(filename, mode, newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    if mode == 'w' or (mode == 'a' and not file_exists):
                        writer.writeheader()
                    for p in problems:
                        if isinstance(p, dict):
                            writer.writerow({k: p.get(k, '') for k in fieldnames})
                print(f"✓ Saved {len(problems)} problems to {filename}")
            except Exception as e:
                print(f"Error saving to CSV without pandas: {e}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def load_scraper_state(self) -> Dict:
        """Load scraper state from scraper_state.json if present."""
        state_path = 'scraper_state.json'
        try:
            if os.path.exists(state_path):
                with open(state_path, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                if isinstance(state, dict):
                    return state
        except Exception:
            pass
        return {}

    def get_last_scraped_id(self) -> str:
        """Return last scraped ps_id from state, or '0' if none."""
        state = self.load_scraper_state()
        return str(state.get('last_ps_id', '0'))
    
    def validate_data(self, problems: List[Dict]) -> Dict:
        """Validate scraped data and return statistics"""
        stats = {
            'total_problems': len(problems),
            'problems_with_all_fields': 0,
            'unique_organizations': set(),
            'unique_themes': set(),
            'unique_categories': set(),
            'problems_by_theme': {},
            'problems_by_category': {}
        }
        
        required_fields = ['ps_id', 'title', 'description', 'organization']
        
        for problem in problems:
            # Count problems with all required fields
            if all(field in problem and problem[field] for field in required_fields):
                stats['problems_with_all_fields'] += 1
            
            # Collect unique values
            if 'organization' in problem:
                stats['unique_organizations'].add(problem['organization'])
            
            if 'theme' in problem:
                theme = problem['theme']
                stats['unique_themes'].add(theme)
                stats['problems_by_theme'][theme] = stats['problems_by_theme'].get(theme, 0) + 1
            
            if 'category' in problem:
                category = problem['category']
                stats['unique_categories'].add(category)
                stats['problems_by_category'][category] = stats['problems_by_category'].get(category, 0) + 1
        
        # Convert sets to lists for JSON serialization
        stats['unique_organizations'] = list(stats['unique_organizations'])
        stats['unique_themes'] = list(stats['unique_themes'])
        stats['unique_categories'] = list(stats['unique_categories'])
        
        return stats

def main():
    """Main function to run the scraper with different modes"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='SIH Problem Statement Scraper')
    parser.add_argument('--start-id', type=str, help='PS ID to start scraping from (e.g., 25010)')
    parser.add_argument('--incremental', action='store_true', help='Only scrape new problems since last run')
    parser.add_argument('--merge', action='store_true', help='Merge with existing data files')
    parser.add_argument('--url', type=str, default='https://sih.gov.in/sih2025PS', help='SIH website URL')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = SIHScraper()
    
    print(f"🚀 Starting SIH scraper for: {args.url}")
    
    # Show current state
    if args.incremental:
        last_id = scraper.get_last_scraped_id()
        if last_id != '0':
            print(f"📋 Last scraped PS ID: {last_id}")
        else:
            print("📋 No previous scraping state found")
    
    print("=" * 50)
    
    # Scrape problems
    problems = scraper.scrape_sih_problems(
        url=args.url,
        start_ps_id=args.start_id,
        incremental=args.incremental
    )
    
    if problems:
        print("\n" + "=" * 50)
        print(f"🎉 Successfully scraped {len(problems)} problem statements!")
        
        # Validate data
        stats = scraper.validate_data(problems)
        print(f"\n📊 Data Statistics:")
        print(f"   • Total problems: {stats['total_problems']}")
        print(f"   • Complete problems: {stats['problems_with_all_fields']}")
        print(f"   • Unique organizations: {len(stats['unique_organizations'])}")
        print(f"   • Unique themes: {len(stats['unique_themes'])}")
        print(f"   • Unique categories: {len(stats['unique_categories'])}")
        
        # Save data
        scraper.save_to_json(problems, 'sih_problems.json', merge_existing=args.merge)
        scraper.save_to_csv(problems, 'sih_problems.csv', merge_existing=args.merge)
        
        # Save statistics
        with open('scraping_stats.json', 'w') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        # Print sample problem
        if problems:
            print(f"\n📋 Sample Problem:")
            sample = problems[0]
            print(f"   ID: {sample.get('ps_id', 'N/A')}")
            print(f"   Title: {sample.get('title', 'N/A')[:80]}...")
            print(f"   Organization: {sample.get('organization', 'N/A')}")
            print(f"   Theme: {sample.get('theme', 'N/A')}")
            print(f"   Category: {sample.get('category', 'N/A')}")
        
        # Show next run suggestion
        state = scraper.load_scraper_state()
        if state.get('last_ps_id'):
            next_id = int(state['last_ps_id']) + 1
            print(f"\n💡 Next time, run: python scraper.py --start-id {next_id}")
            print(f"   Or use: python scraper.py --incremental")
        
    else:
        print("❌ No problems were scraped. Check the URL and website structure.")

# Alternative simple usage functions
def scrape_from_id(start_ps_id: str, url: str = "https://sih.gov.in/sih2025PS"):
    """Simple function to scrape from a specific PS ID"""
    scraper = SIHScraper()
    problems = scraper.scrape_sih_problems(url, start_ps_id=start_ps_id)
    
    if problems:
        scraper.save_to_json(problems, merge_existing=True)
        print(f"✅ Scraped {len(problems)} new problems starting from PS ID {start_ps_id}")
        return problems
    else:
        print("❌ No new problems found")
        return []

def scrape_incremental(url: str = "https://sih.gov.in/sih2025PS"):
    """Simple function for incremental scraping"""
    scraper = SIHScraper()
    problems = scraper.scrape_sih_problems(url, incremental=True)
    
   
    print("ℹ️  No new problems found since last run")
    return []

if __name__ == "__main__":
    main()