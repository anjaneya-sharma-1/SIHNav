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

            # Determine filter threshold if start_ps_id or incremental mode is used
            threshold_num: Optional[int] = None
            if start_ps_id:
                threshold_num = self.extract_numeric_ps_id(start_ps_id)
            if incremental:
                last_id = self.get_last_scraped_id()
                last_num = self.extract_numeric_ps_id(last_id) if last_id else None
                if last_num is not None:
                    inc_threshold = last_num + 1
                    threshold_num = max(threshold_num or inc_threshold, inc_threshold)
            for modal in problem_modals:
                try:
                    # Find the parent table row that contains the modal for submission count extraction
                    table_row = modal.find_parent('tr') if modal else None
                    problem_data = self.extract_problem_data(modal, table_row=table_row)
                    if problem_data:
                        # Apply threshold filtering if configured
                        if threshold_num is not None:
                            current_num = self.extract_numeric_ps_id(
                                problem_data.get('ps_id') or problem_data.get('ps_code', '')
                            )
                            if current_num is None or current_num < threshold_num:
                                continue
                        problems.append(problem_data)
                        print(f"✓ Extracted: {problem_data['ps_id']} - {problem_data['title'][:50]}... (Submissions: {problem_data.get('submission_count', 'N/A')})")
                except Exception as e:
                    print(f"✗ Error extracting problem: {e}")
                    continue
            
            # Update scraper state with the highest PS ID we just saw
            if problems:
                max_seen = None
                for p in problems:
                    num = self.extract_numeric_ps_id(p.get('ps_id') or p.get('ps_code', ''))
                    if num is not None:
                        max_seen = num if max_seen is None else max(max_seen, num)
                if max_seen is not None:
                    self.save_scraper_state({'last_ps_id': str(max_seen), 'updated_at': time.time()})
            
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
        """Save problems to JSON file, with optional merge to avoid duplicates by ps_id/ps_code."""
        try:
            to_save = problems
            if merge_existing and os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        existing = json.load(f)
                    # Index by a stable key
                    def key_fn(item: Dict) -> str:
                        return str(item.get('ps_id') or item.get('ps_code') or item.get('title') or '')
                    merged: Dict[str, Dict] = {}
                    for item in existing if isinstance(existing, list) else []:
                        merged[key_fn(item)] = item
                    for item in problems:
                        merged[key_fn(item)] = item
                    to_save = list(merged.values())
                    print(f"↻ Merged with existing JSON; total {len(to_save)} unique records")
                except Exception as me:
                    print(f"Warning: Failed to merge existing JSON: {me}. Overwriting file.")
                    to_save = problems

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(to_save, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved {len(to_save)} problems to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def save_to_csv(self, problems: List[Dict], filename: str = 'sih_problems.csv', merge_existing: bool = False):
        """Save problems to CSV file, optionally merging with existing rows by ps_id/ps_code/title."""
        try:
            import pandas as pd
            
            df = pd.DataFrame(problems)
            if merge_existing and os.path.exists(filename):
                try:
                    existing_df = pd.read_csv(filename, dtype=str)
                    combined = pd.concat([existing_df, df], ignore_index=True)
                    # Determine a key column; create a derived key to ensure uniqueness
                    def derive_key(row):
                        return str(row.get('ps_id') or row.get('ps_code') or row.get('title') or '')
                    combined['_merge_key'] = combined.apply(derive_key, axis=1)
                    combined = combined.drop_duplicates(subset=['_merge_key'])
                    combined = combined.drop(columns=['_merge_key'])
                    df = combined
                    print(f"↻ Merged with existing CSV; total {len(df)} unique records")
                except Exception as me:
                    print(f"Warning: Failed to merge existing CSV: {me}. Overwriting file.")
            
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"✓ Saved {len(df)} problems to {filename}")
        except ImportError:
            print("pandas not installed. Install with: pip install pandas")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    
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

    # -------------------- Submission counts utilities --------------------
    def fetch_submission_counts_from_listing(self, url: str) -> Dict[str, int]:
        """Scrape the main listing page to build a map of ps_id (numeric as string) -> submission_count.
        Tries to locate header indices for 'PS Code' and 'Submissions'; falls back to positional heuristic.
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            counts: Dict[str, int] = {}

            def find_indices(table):
                head = table.find('thead') or table
                header_row = None
                for tr in head.find_all('tr'):
                    if tr.find('th'):
                        header_row = tr
                        break
                if not header_row:
                    return None, None
                ths = header_row.find_all(['th', 'td'])
                ps_code_idx = None
                submissions_idx = None
                for i, th in enumerate(ths):
                    text = self.clean_text(th.get_text()).lower()
                    if ps_code_idx is None and ('ps code' in text or text == 'ps code' or 'pscode' in text):
                        ps_code_idx = i
                    if submissions_idx is None and ('submission' in text or 'submissions' in text):
                        submissions_idx = i
                return ps_code_idx, submissions_idx

            tables = soup.find_all('table')
            used_table = False
            for table in tables:
                ps_idx, sub_idx = find_indices(table)
                if ps_idx is None or sub_idx is None:
                    continue
                used_table = True
                body = table.find('tbody') or table
                for row in body.find_all('tr'):
                    tds = row.find_all('td')
                    if len(tds) <= max(ps_idx, sub_idx):
                        continue
                    ps_code_text = self.clean_text(tds[ps_idx].get_text())
                    sub_text = self.clean_text(tds[sub_idx].get_text())
                    if not ps_code_text:
                        continue
                    num = self.extract_numeric_ps_id(ps_code_text)
                    if num is None:
                        continue
                    try:
                        value = int(sub_text)
                        counts[str(num)] = value
                        print(f"↪ Found PS ID on listing: {num} with submissions={value}")
                    except Exception:
                        counts[str(num)] = 0
                        print(f"↪ Found PS ID on listing: {num} with submissions=0 (non-integer '{sub_text}')")

            # Fallback heuristic if header-based parsing failed
            if not counts and not used_table:
                for row in soup.find_all('tr'):
                    tds = row.find_all('td')
                    if len(tds) < 6:
                        continue
                    ps_code_text = self.clean_text(tds[4].get_text())
                    sub_text = self.clean_text(tds[5].get_text())
                    if not ps_code_text:
                        continue
                    num = self.extract_numeric_ps_id(ps_code_text)
                    if num is None:
                        continue
                    try:
                        value = int(sub_text)
                        counts[str(num)] = value
                        print(f"↪ Found PS ID on listing (fallback): {num} with submissions={value}")
                    except Exception:
                        counts[str(num)] = 0
                        print(f"↪ Found PS ID on listing (fallback): {num} with submissions=0 (non-integer '{sub_text}')")

            print(f"Found submission counts for {len(counts)} PS entries from listing page")
            return counts
        except Exception as e:
            print(f"Error fetching submission counts: {e}")
            return {}

    def write_submission_counts_for_results(self, results_path: str, url: str, out_path: str = 'submission_counts.tmp.json') -> int:
        """Read results.json, compute submission counts for its ps_ids from listing page, and write a temp JSON file.

        Returns the number of entries written.
        """
        try:
            if not os.path.exists(results_path):
                print(f"results file not found: {results_path}")
                return 0
            with open(results_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list):
                print("results.json is not a list; skipping counts generation")
                return 0

            counts_map = self.fetch_submission_counts_from_listing(url)
            if not counts_map:
                print("No submission counts found on listing page")
                return 0

            output: Dict[str, int] = {}
            for rec in data:
                if not isinstance(rec, dict):
                    continue
                ps_id = str(rec.get('ps_id') or '').strip()
                num = self.extract_numeric_ps_id(ps_id)
                if num is None:
                    continue
                key = str(num)
                if key in counts_map:
                    output[ps_id] = counts_map[key]

            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            print(f"✓ Wrote submission counts for {len(output)} PS IDs to {out_path}")
            return len(output)
        except Exception as e:
            print(f"Error writing submission counts: {e}")
            return 0

    def merge_submission_counts_into_results(self, results_path: str, url: str) -> int:
        """Merge submission counts by scraping listing rows and reusing extract_row_data. Returns updated count."""
        try:
            if not os.path.exists(results_path):
                print(f"results file not found: {results_path}")
                return 0
            with open(results_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list):
                print("results.json is not a list; aborting merge")
                return 0

            # Build counts map by iterating listing rows and calling extract_row_data
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                print(f"Error fetching listing for merge: {e}")
                return 0

            counts_map: Dict[str, int] = {}
            rows = soup.find_all('tr')
            total_rows = 0
            for row in rows:
                tds = row.find_all('td')
                if len(tds) < 6:
                    continue
                total_rows += 1
                tmp: Dict = {}
                # Reuse row extraction to populate ps_code and submission_count
                try:
                    self.extract_row_data(row, tmp)
                except Exception:
                    continue
                # Derive numeric key and submission count
                ps_code_text = tmp.get('ps_code') or self.clean_text(tds[4].get_text())
                num = self.extract_numeric_ps_id(ps_code_text)
                if num is None:
                    continue
                sub_val = tmp.get('submission_count')
                try:
                    sub_val = int(sub_val) if sub_val is not None else int(self.clean_text(tds[5].get_text()))
                except Exception:
                    sub_val = 0
                counts_map[str(num)] = sub_val
                print(f"↪ Row-derived PS {num} submissions={sub_val}")

            if not counts_map:
                print("No submission counts found on listing page via rows; nothing to merge")
                return 0

            updated = 0
            for rec in data:
                if not isinstance(rec, dict):
                    continue
                # Support numeric-only ps_id (e.g., "25001") or prefixed (e.g., "SIH25001")
                ps_id_value = rec.get('ps_id')
                ps_id = str(ps_id_value if ps_id_value is not None else '').strip()
                num = self.extract_numeric_ps_id(ps_id)
                if num is None:
                    continue
                key = str(num)
                if key in counts_map:
                    new_val = counts_map[key]
                    if rec.get('submission_count') != new_val:
                        rec['submission_count'] = new_val
                        updated += 1
                        print(f"✓ Updated submission_count for PS {ps_id or num}: {new_val}")
                    else:
                        print(f"= No change for PS {ps_id or num}: already {new_val}")

            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Merged submission counts into results.json for {updated} records")
            return updated
        except Exception as e:
            print(f"Error merging submission counts: {e}")
            return 0

    def normalize_ps_ids_in_results(self, results_path: str, prefix: str = 'SIH') -> int:
        """Normalize ps_id values in results.json to the format '<prefix><digits>', e.g., 'SIH25001'. Returns count updated."""
        try:
            if not os.path.exists(results_path):
                print(f"results file not found: {results_path}")
                return 0
            with open(results_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list):
                print("results.json is not a list; aborting normalization")
                return 0

            updated = 0
            for rec in data:
                if not isinstance(rec, dict):
                    continue
                raw = rec.get('ps_id')
                text = str(raw if raw is not None else '').strip()
                num = self.extract_numeric_ps_id(text)
                if num is None:
                    continue
                normalized = f"{prefix}{num}"
                if text != normalized:
                    rec['ps_id'] = normalized
                    updated += 1

            if updated:
                with open(results_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Normalized ps_id format for {updated} records in results.json")
            return updated
        except Exception as e:
            print(f"Error normalizing ps_id values: {e}")
            return 0

    # -------------------- Merge with server + final schema --------------------
    def _coerce_list(self, value) -> List[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(v).strip() for v in value if str(v).strip()]
        if isinstance(value, str):
            parts = [p.strip() for p in value.split(',')]
            return [p for p in parts if p]
        return []

    def normalize_to_final_schema(self, record: Dict) -> Dict:
        """Normalize any input record to the required final schema."""
        return {
            'ps_id': record.get('ps_id', ''),
            'title': record.get('title', ''),
            'summary': record.get('summary', ''),
            'description': record.get('description', ''),
            'difficulty': record.get('difficulty', ''),
            'technology': self._coerce_list(record.get('technology', [])),
            'stakeholders': self._coerce_list(record.get('stakeholders', [])),
            'impact_area': self._coerce_list(record.get('impact_area', [])),
            'data_resource_type': self._coerce_list(record.get('data_resource_type', [])),
            'solution_type': record.get('solution_type', ''),
            'organization': record.get('organization', ''),
            'department': record.get('department', ''),
            'category': record.get('category', ''),
            'theme': record.get('theme', ''),
        }

    def transform_scraped_to_final(self, scraped: Dict) -> Dict:
        """Transform a scraped record to the final schema with sensible defaults."""
        base = {
            'ps_id': scraped.get('ps_id', ''),
            'title': scraped.get('title', ''),
            'summary': scraped.get('summary', ''),
            'description': scraped.get('description', ''),
            'difficulty': scraped.get('difficulty', ''),
            'technology': scraped.get('technology', []),
            'stakeholders': scraped.get('stakeholders', []),
            'impact_area': scraped.get('impact_area', []),
            'data_resource_type': scraped.get('data_resource_type', []),
            'solution_type': scraped.get('solution_type', ''),
            'organization': scraped.get('organization', ''),
            'department': scraped.get('department', ''),
            'category': scraped.get('category', ''),
            'theme': scraped.get('theme', ''),
        }
        return self.normalize_to_final_schema(base)

    def _merge_lists(self, a: List[str], b: List[str]) -> List[str]:
        seen = set()
        result: List[str] = []
        for v in (a or []):
            sv = str(v).strip()
            if sv and sv not in seen:
                seen.add(sv)
                result.append(sv)
        for v in (b or []):
            sv = str(v).strip()
            if sv and sv not in seen:
                seen.add(sv)
                result.append(sv)
        return result

    def _merge_records_final(self, prefer: Dict, fallback: Dict) -> Dict:
        """Merge two final-schema records, preferring non-empty values from 'prefer'."""
        merged = {}
        for key in ['ps_id', 'title', 'summary', 'description', 'difficulty', 'solution_type', 'organization', 'department', 'category', 'theme']:
            merged[key] = prefer.get(key) or fallback.get(key) or ''
        # List fields: union
        merged['technology'] = self._merge_lists(prefer.get('technology', []), fallback.get('technology', []))
        merged['stakeholders'] = self._merge_lists(prefer.get('stakeholders', []), fallback.get('stakeholders', []))
        merged['impact_area'] = self._merge_lists(prefer.get('impact_area', []), fallback.get('impact_area', []))
        merged['data_resource_type'] = self._merge_lists(prefer.get('data_resource_type', []), fallback.get('data_resource_type', []))
        return merged

    def _derive_merge_key(self, record: Dict) -> str:
        ps_id = record.get('ps_id') or ''
        num = self.extract_numeric_ps_id(ps_id)
        if num is not None:
            return f"ps:{num}"
        alt = record.get('ps_code') or record.get('title') or ''
        return f"alt:{alt}"

    def merge_scraped_and_server(self, scraped: List[Dict], server_data) -> List[Dict]:
        """Merge scraped data with server-generated data into the final schema, keyed by ps_id/code/title."""
        # Prepare server list
        server_list: List[Dict] = []
        if isinstance(server_data, list):
            server_list = server_data
        elif isinstance(server_data, dict):
            # allow either a single record or an envelope with 'data'
            if 'data' in server_data and isinstance(server_data['data'], list):
                server_list = server_data['data']
            else:
                server_list = [server_data]

        # Index server by merge key (normalized to final schema)
        server_map: Dict[str, Dict] = {}
        for rec in server_list:
            final_rec = self.normalize_to_final_schema(rec)
            key = self._derive_merge_key(final_rec)
            server_map[key] = final_rec

        # Merge scraped
        merged_map: Dict[str, Dict] = dict(server_map)
        for s in scraped:
            scraped_final = self.transform_scraped_to_final(s)
            key = self._derive_merge_key({**s, **scraped_final})
            if key in merged_map:
                # Prefer server values, fallback to scraped
                merged_map[key] = self._merge_records_final(merged_map[key], scraped_final)
            else:
                merged_map[key] = scraped_final

        return list(merged_map.values())

    def save_results_json(self, records: List[Dict], filename: str = 'results.json'):
        """Save final merged records to results.json, merging with existing to avoid duplicates."""
        try:
            existing: List[Dict] = []
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        loaded = json.load(f)
                        if isinstance(loaded, list):
                            existing = loaded
                except Exception:
                    existing = []
            # Merge with existing
            combined = self.merge_scraped_and_server([], existing)
            combined = self.merge_scraped_and_server(combined, records)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(combined, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving results.json: {e}")

    # -------------------- State management helpers --------------------
    def load_scraper_state(self) -> Dict:
        """Load scraper state from local file."""
        state_file = 'scraper_state.json'
        try:
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load scraper state: {e}")
        return {}

    def save_scraper_state(self, state: Dict):
        """Persist scraper state to local file."""
        state_file = 'scraper_state.json'
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Failed to save scraper state: {e}")

    def get_last_scraped_id(self) -> str:
        """Return the last scraped PS ID as a string, preferring results.json; fallback to state; '0' if unknown."""
        try:
            last_from_results = self.get_last_psid_from_results()
            if last_from_results is not None:
                return str(last_from_results)
        except Exception:
            pass
        state = self.load_scraper_state()
        return state.get('last_ps_id', '0')

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

    def get_last_psid_from_results(self) -> Optional[int]:
        """Scan results.json and return the maximum numeric ps_id if available."""
        filename = 'results.json'
        if not os.path.exists(filename):
            return None
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list):
                return None
            max_num: Optional[int] = None
            for rec in data:
                if not isinstance(rec, dict):
                    continue
                num = self.extract_numeric_ps_id(rec.get('ps_id') or rec.get('ps_code'))
                if num is not None:
                    max_num = num if max_num is None else max(max_num, num)
            return max_num
        except Exception:
            return None

def main():
    """Main function to run the scraper with different modes"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='SIH Problem Statement Scraper')
    parser.add_argument('--start-id', type=str, help='PS ID to start scraping from (e.g., 25010)')
    parser.add_argument('--incremental', action='store_true', help='Only scrape new problems since last run')
    parser.add_argument('--merge', action='store_true', help='Merge with existing data files')
    parser.add_argument('--url', type=str, default='https://sih.gov.in/sih2025PS', help='SIH website URL')
    parser.add_argument('--gen-submission-counts', action='store_true', help='Generate a temp file with submission counts for PS IDs in results.json')
    parser.add_argument('--merge-submission-counts', action='store_true', help="Merge submission counts into results.json under 'submission_count'")
    parser.add_argument('--normalize-psids', action='store_true', help='Normalize ps_id values in results.json to SIH<number> format')
    parser.add_argument('--server-json', type=str, help='Path to server-generated JSON to merge into results.json')
    
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
    
    # Generate submission counts temp file and exit if requested
    if args.gen_submission_counts:
        scraper.write_submission_counts_for_results('results.json', args.url, 'submission_counts.tmp.json')
        return

    # Normalize ps_id values in results.json and exit if requested
    if args.normalize_psids:
        scraper.normalize_ps_ids_in_results('results.json', prefix='SIH')
        return

    if args.merge_submission_counts:
        scraper.merge_submission_counts_into_results('results.json', args.url)
        return

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
        
        # Always append to results.json in final schema, merging with server JSON if provided
        try:
            server_data = []
            if args.server_json and os.path.exists(args.server_json):
                with open(args.server_json, 'r', encoding='utf-8') as f:
                    server_data = json.load(f)
            final_records = scraper.merge_scraped_and_server(problems, server_data)
            scraper.save_results_json(final_records, 'results.json')
            print(f"📦 results.json updated with {len(final_records)} merged records")
        except Exception as e:
            print(f"Warning: Failed to update results.json: {e}")

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
    
    if problems:
        scraper.save_to_json(problems, merge_existing=True)
        print(f"✅ Scraped {len(problems)} new problems since last run")
        return problems
    else:
        print("ℹ️  No new problems found since last run")
        return []

def run_and_merge(server_json_path: str, url: str = "https://sih.gov.in/sih2025PS") -> List[Dict]:
    """Helper to run incremental scraping and merge with a server JSON into results.json."""
    scraper = SIHScraper()
    problems = scraper.scrape_sih_problems(url, incremental=True)
    server_data = []
    if os.path.exists(server_json_path):
        try:
            with open(server_json_path, 'r', encoding='utf-8') as f:
                server_data = json.load(f)
        except Exception as e:
            print(f"Warning: Could not read server JSON at {server_json_path}: {e}")
    final_records = scraper.merge_scraped_and_server(problems, server_data)
    scraper.save_results_json(final_records, 'results.json')
    print(f"📦 results.json updated with {len(final_records)} merged records")
    return final_records

if __name__ == "__main__":
    main()