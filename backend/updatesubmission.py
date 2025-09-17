import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from typing import Dict, List, Optional
import argparse

class SubmissionUpdater:
    """
    Class to update submission counts in results.json by scraping from SIH website
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        # Remove extra whitespace and newlines
        cleaned = ' '.join(text.strip().split())
        return cleaned
    
    def extract_numeric_ps_id(self, value: Optional[str]) -> Optional[int]:
        """Extract the numeric portion of a PS identifier (e.g., 'SIH25001' -> 25001)."""
        if not value:
            return None
        match = re.search(r'(\d{3,})', str(value))
        if not match:
            return None
        try:
            return int(match.group(1))
        except Exception:
            return None
    
    def scrape_submission_counts(self, url: str = "https://sih.gov.in/sih2025PS") -> Dict[str, int]:
        """
        Scrape submission counts from the SIH website listing page
        Returns a dictionary mapping PS ID to submission count
        """
        try:
            print(f"🌐 Fetching submission counts from: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            submission_counts = {}
            
            # Method 1: Try to find table headers and use them to identify columns
            tables = soup.find_all('table')
            successful_parse = False
            
            for table in tables:
                # Find header row
                header_row = None
                thead = table.find('thead')
                if thead:
                    header_row = thead.find('tr')
                else:
                    # Look for first row with th elements
                    for tr in table.find_all('tr'):
                        if tr.find('th'):
                            header_row = tr
                            break
                
                if not header_row:
                    continue
                
                # Identify column positions
                headers = header_row.find_all(['th', 'td'])
                ps_code_idx = None
                submissions_idx = None
                
                for i, header in enumerate(headers):
                    header_text = self.clean_text(header.get_text()).lower()
                    if 'ps code' in header_text or 'pscode' in header_text or header_text == 'ps code':
                        ps_code_idx = i
                    elif 'submission' in header_text and submissions_idx is None:
                        submissions_idx = i
                
                if ps_code_idx is None or submissions_idx is None:
                    print(f"⚠️  Could not find PS Code ({ps_code_idx}) or Submissions ({submissions_idx}) columns in table headers")
                    continue
                
                print(f"✓ Found PS Code column at index {ps_code_idx}, Submissions at index {submissions_idx}")
                
                # Parse data rows
                tbody = table.find('tbody') or table
                rows = tbody.find_all('tr')
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) <= max(ps_code_idx, submissions_idx):
                        continue
                    
                    try:
                        ps_code_text = self.clean_text(cells[ps_code_idx].get_text())
                        submission_text = self.clean_text(cells[submissions_idx].get_text())
                        
                        if not ps_code_text:
                            continue
                        
                        # Extract numeric PS ID
                        numeric_id = self.extract_numeric_ps_id(ps_code_text)
                        if numeric_id is None:
                            continue
                        
                        # Convert submission count to integer
                        try:
                            submission_count = int(submission_text)
                        except (ValueError, TypeError):
                            submission_count = 0
                        
                        ps_id = str(numeric_id)
                        submission_counts[ps_id] = submission_count
                        print(f"   📊 PS {ps_id}: {submission_count} submissions")
                        
                    except Exception as e:
                        print(f"   ⚠️  Error parsing row: {e}")
                        continue
                
                if submission_counts:
                    successful_parse = True
                    break
            
            # Method 2: Fallback heuristic if header-based parsing failed
            if not successful_parse:
                print("📋 Trying fallback parsing method...")
                all_rows = soup.find_all('tr')
                
                for row in all_rows:
                    cells = row.find_all('td')
                    if len(cells) < 6:  # Minimum expected columns
                        continue
                    
                    try:
                        # Based on typical structure: Serial | Organization | Title | Category | PS Code | Submissions | Theme
                        ps_code_text = self.clean_text(cells[4].get_text())  # PS Code usually at index 4
                        submission_text = self.clean_text(cells[5].get_text())  # Submissions usually at index 5
                        
                        if not ps_code_text:
                            continue
                        
                        numeric_id = self.extract_numeric_ps_id(ps_code_text)
                        if numeric_id is None:
                            continue
                        
                        try:
                            submission_count = int(submission_text)
                        except (ValueError, TypeError):
                            submission_count = 0
                        
                        ps_id = str(numeric_id)
                        submission_counts[ps_id] = submission_count
                        print(f"   📊 PS {ps_id}: {submission_count} submissions (fallback)")
                        
                    except Exception as e:
                        continue
            
            print(f"✅ Successfully scraped submission counts for {len(submission_counts)} problem statements")
            return submission_counts
            
        except requests.RequestException as e:
            print(f"❌ Error fetching website: {e}")
            return {}
        except Exception as e:
            print(f"❌ Error parsing submission counts: {e}")
            return {}
    
    def load_results_json(self, file_path: str = "results.json") -> List[Dict]:
        """Load the results.json file"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ Results file not found: {file_path}")
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                print(f"❌ Results file is not a list: {file_path}")
                return []
            
            print(f"📂 Loaded {len(data)} records from {file_path}")
            return data
            
        except Exception as e:
            print(f"❌ Error loading results file: {e}")
            return []
    
    def save_results_json(self, data: List[Dict], file_path: str = "results.json") -> bool:
        """Save the updated data back to results.json"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Successfully saved updated data to {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving results file: {e}")
            return False
    
    def update_submission_counts(self, 
                               submission_counts: Dict[str, int], 
                               results_data: List[Dict],
                               force_update: bool = False) -> tuple[int, int]:
        """
        Update submission counts in results data
        Returns (updated_count, total_count)
        """
        updated_count = 0
        total_count = len(results_data)
        
        for record in results_data:
            if not isinstance(record, dict):
                continue
            
            ps_id = record.get('ps_id', '')
            if not ps_id:
                continue
            
            # Extract numeric ID for matching
            numeric_id = self.extract_numeric_ps_id(str(ps_id))
            if numeric_id is None:
                continue
            
            lookup_key = str(numeric_id)
            
            if lookup_key in submission_counts:
                new_count = submission_counts[lookup_key]
                current_count = record.get('submission_count', 0)
                
                if force_update or current_count != new_count:
                    record['submission_count'] = new_count
                    updated_count += 1
                    
                    status_emoji = "🔄" if current_count != new_count else "✓"
                    print(f"   {status_emoji} PS {ps_id}: {current_count} → {new_count}")
                else:
                    print(f"   = PS {ps_id}: {current_count} (no change)")
            else:
                print(f"   ⚠️  PS {ps_id}: No submission count found on website")
        
        return updated_count, total_count
    
    def create_backup(self, file_path: str = "results.json") -> str:
        """Create a backup of the results file before updating"""
        try:
            if not os.path.exists(file_path):
                return ""
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.backup_{timestamp}"
            
            with open(file_path, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            
            print(f"💾 Created backup: {backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"⚠️  Warning: Could not create backup: {e}")
            return ""
    
    def run_update(self, 
                   url: str = "https://sih.gov.in/sih2025PS",
                   results_file: str = "results.json",
                   create_backup: bool = True,
                   force_update: bool = False,
                   dry_run: bool = False) -> bool:
        """
        Main method to run the submission count update process
        """
        print("🚀 Starting submission count update process...")
        print("=" * 60)
        
        # Create backup if requested
        if create_backup and not dry_run:
            self.create_backup(results_file)
        
        # Load current results
        results_data = self.load_results_json(results_file)
        if not results_data:
            return False
        
        # Scrape submission counts from website
        submission_counts = self.scrape_submission_counts(url)
        if not submission_counts:
            print("❌ No submission counts found. Update aborted.")
            return False
        
        print(f"\n📊 Updating submission counts...")
        print("-" * 40)
        
        # Update the data
        updated_count, total_count = self.update_submission_counts(
            submission_counts, results_data, force_update
        )
        
        print("-" * 40)
        print(f"📈 Summary: Updated {updated_count} of {total_count} records")
        
        # Save updated data (unless dry run)
        if not dry_run:
            if self.save_results_json(results_data, results_file):
                print("✅ Submission count update completed successfully!")
                return True
            else:
                print("❌ Failed to save updated data!")
                return False
        else:
            print("🔍 Dry run completed - no files were modified")
            return True
    
    def generate_report(self, results_file: str = "results.json") -> None:
        """Generate a summary report of submission counts"""
        results_data = self.load_results_json(results_file)
        if not results_data:
            return
        
        total_problems = len(results_data)
        problems_with_submissions = 0
        total_submissions = 0
        max_submissions = 0
        max_ps_id = ""
        
        submission_distribution = {}
        
        for record in results_data:
            if not isinstance(record, dict):
                continue
            
            submission_count = record.get('submission_count', 0)
            ps_id = record.get('ps_id', 'Unknown')
            
            if submission_count > 0:
                problems_with_submissions += 1
                total_submissions += submission_count
                
                if submission_count > max_submissions:
                    max_submissions = submission_count
                    max_ps_id = ps_id
            
            # Group by submission count ranges
            if submission_count == 0:
                range_key = "0 submissions"
            elif submission_count <= 10:
                range_key = "1-10 submissions"
            elif submission_count <= 50:
                range_key = "11-50 submissions"
            elif submission_count <= 100:
                range_key = "51-100 submissions"
            else:
                range_key = "100+ submissions"
            
            submission_distribution[range_key] = submission_distribution.get(range_key, 0) + 1
        
        print("\n" + "=" * 60)
        print("📊 SUBMISSION COUNTS REPORT")
        print("=" * 60)
        print(f"Total Problem Statements: {total_problems}")
        print(f"Problems with Submissions: {problems_with_submissions}")
        print(f"Problems without Submissions: {total_problems - problems_with_submissions}")
        print(f"Total Submissions: {total_submissions}")
        
        if problems_with_submissions > 0:
            avg_submissions = total_submissions / problems_with_submissions
            print(f"Average Submissions (non-zero): {avg_submissions:.2f}")
        
        print(f"Highest Submissions: {max_submissions} (PS {max_ps_id})")
        
        print(f"\n📈 Distribution:")
        for range_key, count in sorted(submission_distribution.items()):
            percentage = (count / total_problems) * 100
            print(f"  {range_key}: {count} ({percentage:.1f}%)")
        
        print("=" * 60)


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Update submission counts in results.json from SIH website')
    
    parser.add_argument('--url', type=str, default='https://sih.gov.in/sih2025PS',
                       help='SIH website URL to scrape from')
    parser.add_argument('--results-file', type=str, default='results.json',
                       help='Path to results.json file to update')
    parser.add_argument('--no-backup', action='store_true',
                       help='Skip creating backup before update')
    parser.add_argument('--force', action='store_true',
                       help='Force update even if submission count is the same')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without making changes')
    parser.add_argument('--report', action='store_true',
                       help='Generate summary report of submission counts')
    
    args = parser.parse_args()
    
    updater = SubmissionUpdater()
    
    if args.report:
        updater.generate_report(args.results_file)
        return
    
    success = updater.run_update(
        url=args.url,
        results_file=args.results_file,
        create_backup=not args.no_backup,
        force_update=args.force,
        dry_run=args.dry_run
    )
    
    if success:
        # Generate report after successful update
        if not args.dry_run:
            print("\n")
            updater.generate_report(args.results_file)
    else:
        exit(1)


if __name__ == "__main__":
    main()