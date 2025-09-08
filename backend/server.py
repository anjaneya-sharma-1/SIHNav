import requests
import json
import time
import os
import random
from typing import List, Dict
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("ℹ️  python-dotenv not installed. Using system environment variables only.")

try:
    # Import scraper utilities for scraping and merging
    from .scraper import SIHScraper  # if run as a module
except ImportError:
    from scraper import SIHScraper  # if run directly from backend/

# -----------------------------
# CONFIGURATION
# -----------------------------
# Gemini configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-lite")
# Batching configuration for Gemini Flash Lite (30 requests per minute)
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "30"))  # 30 requests per batch
BATCH_INTERVAL_SEC = int(os.environ.get("BATCH_INTERVAL_SEC", "60"))  # Wait 60 seconds between batches
MAX_RETRIES = int(os.environ.get("LLM_MAX_RETRIES", "3"))
BACKOFF_BASE = float(os.environ.get("LLM_BACKOFF_BASE", "2.0"))
BACKOFF_INITIAL = float(os.environ.get("LLM_BACKOFF_INITIAL", "1.0"))
JITTER_SEC = float(os.environ.get("LLM_JITTER_SEC", "0.3"))

# Initialize Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️  Warning: GEMINI_API_KEY not set. Please set it in environment variables.")

# -----------------------------
# TAG SETUP (Fixed categories)
# -----------------------------
TAGS = {
    "Difficulty": ["Easy", "Med", "Hard"],
    "Technology": [
        "Artificial Intelligence (AI)", "Machine Learning (ML)", "Deep Learning (DL)",
        "Natural Language Processing (NLP)", "Computer Vision", "Robotics",
        "IoT (Internet of Things)", "Blockchain", "Augmented Reality (AR)",
        "Virtual Reality (VR)", "Frontend Dev", "Backend Dev", "Full Stack Development",
        "Web Development", "Mobile App Development", "Game Dev", "Cloud Computing",
        "Edge Computing", "Data Analytics", "Cybersecurity", "GIS / Remote Sensing",
        "Embedded Systems"
    ],
    "Stakeholders": [
        "Government Agencies", "NGOs", "Farmers", "Students / Teachers", "Doctors / Patients",
        "Industry / Enterprises", "Local Communities", "Citizens", "Travelers",
        "Law Enforcement", "Military / Defense"
    ],
    "Impact Area": [
        "Cost Reduction", "Efficiency Improvement", "Accessibility", "Sustainability",
        "Inclusivity", "Transparency", "Security", "Safety", "Awareness & Education",
        "Productivity"
    ],
    "Data / Resource Type": [
        "Open Data", "Sensor Data", "Image Data", "Video Data", "Text Data", "Audio Data",
        "Social Media Data", "Satellite Data", "Geospatial Data", "Real-time Streaming"
    ],
    "Solution Type":[
        "Mobile Solutions","Web Solutions","Mobile and Web Solutions"
    ]
}

# -----------------------------
# PROMPT BUILDER
# -----------------------------
def build_prompt(problem: dict):
    instructions = """
You are an expert classifier. 
Your task is to:
1. Generate a short summary (2-3 sentences) of the problem statement.
2. Assign tags to the problem under these fixed categories:

- Difficulty: Easy, Med, Hard
- Technology: Choose one or more relevant items from the list provided.
- Stakeholders: Choose one or more.
- Impact Area: Choose one or more.
- Data / Resource Type: Choose one or more.
- Solution Type: Choose one or none.

Rules:
- Only choose tags from the provided lists.
- Return the output strictly in JSON format.
- If no tag is relevant in a category, return an empty list for that category (except Solution Type which must be one of the four).
- The JSON must contain these keys: summary, difficulty, technology, stakeholders, impact_area, data_resource_type, solution_type.
- Don't write any extra text. Only return the JSON.
Now classify the following problem statement.
"""

    problem_text = f"""
Problem ID: {problem.get("ps_id")}
Title: {problem.get("title")}
Description: {problem.get("description")}
Organization: {problem.get("organization")}
Department: {problem.get("department")}
Theme: {problem.get("theme")}
Category: {problem.get("category")}
"""

    return f"{instructions}\n{problem_text}\n\nValid Tags:\n{json.dumps(TAGS, indent=2)}\n\nOutput JSON:"

# -----------------------------
# CALL GEMINI API
# -----------------------------
def classify_problem(problem: dict, model: str = MODEL):
    """Classify a single problem using Gemini API"""
    try:
        model_instance = genai.GenerativeModel(model)
        prompt = build_prompt(problem)
        
        response = model_instance.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=1024,
            )
        )
        
        if not response.text:
            print(f"Empty response from Gemini for problem {problem.get('ps_id')}")
            return None
            
        output_text = response.text.strip()
        
        # Some models wrap in code fences → extract clean JSON
        if "```" in output_text:
            if "```json" in output_text:
                output_text = output_text.split("```json")[-1].split("```")[0].strip()
            else:
                output_text = output_text.split("```")[-2].strip()

        output_json = json.loads(output_text)
        
        # Attach ps_id for easy mapping
        output_json["ps_id"] = problem.get("ps_id")
        return output_json

    except Exception as e:
        print(f"Error classifying problem {problem.get('ps_id')}: {e}")
        return None

def classify_batch(problems: List[dict], model: str = MODEL) -> List[dict]:
    """Classify a batch of problems concurrently using Gemini API"""
    results = []
    
    def classify_single(problem):
        return classify_problem(problem, model)
    
    # Use ThreadPoolExecutor for concurrent requests within the batch
    with ThreadPoolExecutor(max_workers=min(10, len(problems))) as executor:
        future_to_problem = {executor.submit(classify_single, problem): problem for problem in problems}
        
        for future in as_completed(future_to_problem):
            problem = future_to_problem[future]
            try:
                result = future.result()
                if result is not None:
                    results.append(result)
                else:
                    print(f"⚠️  Failed to classify problem {problem.get('ps_id')}")
            except Exception as e:
                print(f"⚠️  Exception classifying problem {problem.get('ps_id')}: {e}")
    
    return results

# -----------------------------
# Batch processing and retry helpers
# -----------------------------
def classify_with_retries(problem: Dict, model: str = MODEL, max_retries: int = MAX_RETRIES) -> Dict:
    """Classify a single problem with retries (fallback for individual problems)"""
    for attempt in range(max(1, int(max_retries))):
        result = classify_problem(problem, model=model)
        if result is not None:
            return result
        # Backoff before retrying
        sleep_time = BACKOFF_INITIAL * (BACKOFF_BASE ** attempt) + random.uniform(0, JITTER_SEC)
        sleep_time = min(sleep_time, 30.0)
        print(f"⏳ Retry {attempt + 1}/{max_retries} after {sleep_time:.2f}s due to previous error")
        time.sleep(sleep_time)
    return None

def classify_batch_with_retries(problems: List[Dict], model: str = MODEL, max_retries: int = MAX_RETRIES) -> List[Dict]:
    """Classify a batch of problems with retries"""
    for attempt in range(max(1, int(max_retries))):
        results = classify_batch(problems, model=model)
        if len(results) >= len(problems) * 0.8:  # Success if at least 80% classified
            return results
        
        # Retry failed problems
        classified_ids = {r.get("ps_id") for r in results}
        failed_problems = [p for p in problems if p.get("ps_id") not in classified_ids]
        
        if not failed_problems:
            return results
            
        sleep_time = BACKOFF_INITIAL * (BACKOFF_BASE ** attempt) + random.uniform(0, JITTER_SEC)
        sleep_time = min(sleep_time, 30.0)
        print(f"⏳ Batch retry {attempt + 1}/{max_retries} after {sleep_time:.2f}s for {len(failed_problems)} failed problems")
        time.sleep(sleep_time)
        problems = failed_problems  # Only retry the failed ones
    
    return results if 'results' in locals() else []

def process_problems_in_batches(problems: List[Dict], model: str = MODEL) -> List[Dict]:
    """Process problems in batches respecting Gemini rate limits"""
    all_results = []
    total_batches = (len(problems) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for i in range(0, len(problems), BATCH_SIZE):
        batch_num = (i // BATCH_SIZE) + 1
        batch = problems[i:i + BATCH_SIZE]
        
        print(f"🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} problems)...")
        
        batch_results = classify_batch_with_retries(batch, model=model)
        all_results.extend(batch_results)
        
        print(f"✅ Batch {batch_num} completed: {len(batch_results)}/{len(batch)} problems classified successfully")
        
        # Wait between batches (except for the last batch)
        if i + BATCH_SIZE < len(problems):
            print(f"⏳ Waiting {BATCH_INTERVAL_SEC} seconds before next batch...")
            time.sleep(BATCH_INTERVAL_SEC)
    
    return all_results

# -----------------------------
# ORCHESTRATION: Run scraper, classify, and write results.json
# -----------------------------
def build_final_record_from_classification(problem: Dict, tags: Dict) -> Dict:
    """Combine scraped fields and classification into the final schema record."""
    return {
        "ps_id": problem.get("ps_id", ""),
        "title": problem.get("title", ""),
        "summary": (tags or {}).get("summary", ""),
        "description": problem.get("description", ""),
        "difficulty": (tags or {}).get("difficulty", ""),
        "technology": (tags or {}).get("technology", []) or [],
        "stakeholders": (tags or {}).get("stakeholders", []) or [],
        "impact_area": (tags or {}).get("impact_area", []) or [],
        "data_resource_type": (tags or {}).get("data_resource_type", []) or [],
        "solution_type": (tags or {}).get("solution_type", ""),
        "organization": problem.get("organization", ""),
        "department": problem.get("department", ""),
        "category": problem.get("category", ""),
        "theme": problem.get("theme", ""),
        "submission_count": problem.get("submission_count", 0),
    }

def run_pipeline(url: str = "https://sih.gov.in/sih2025PS") -> List[Dict]:
    """Complete pipeline: Scrape new problems, classify them, and save to results.json."""
    
    print("🚀 Starting SIH Problem Classification Pipeline")
    print("=" * 60)
    
    # Step 1: Scrape new problems
    scraper = SIHScraper()
    print("🔎 Scraping new problems from SIH website...")
    problems = scraper.scrape_sih_problems(url, incremental=True)
    
    if not problems:
        print("ℹ️  No new problems found. All up to date!")
        return []

    print(f"📋 Found {len(problems)} new problems to classify")
    print(f"📊 Batch configuration: {BATCH_SIZE} problems per batch, {BATCH_INTERVAL_SEC}s between batches")
    
    # Estimate total time
    estimated_batches = (len(problems) + BATCH_SIZE - 1) // BATCH_SIZE
    estimated_time = (estimated_batches - 1) * BATCH_INTERVAL_SEC / 60  # in minutes
    print(f"⏱️  Estimated completion time: ~{estimated_time:.1f} minutes")
    print("=" * 60)
    
    # Step 2: Classify problems using Gemini
    start_time = time.time()
    print("🧠 Starting classification using Gemini Flash...")
    
    all_classifications = process_problems_in_batches(problems, model=MODEL)
    
    # Step 3: Build final records
    print("📝 Building final records...")
    server_records: List[Dict] = []
    classification_dict = {c.get("ps_id"): c for c in all_classifications}
    
    for p in problems:
        ps_id = p.get("ps_id")
        tags = classification_dict.get(ps_id)
        if tags is None:
            print(f"⚠️  Skipping problem {ps_id} - no classification found")
            continue
        server_records.append(build_final_record_from_classification(p, tags))

    elapsed_time = (time.time() - start_time) / 60
    print(f"🏁 Classification completed in {elapsed_time:.2f} minutes")
    print(f"📈 Success rate: {len(server_records)}/{len(problems)} ({len(server_records)/len(problems)*100:.1f}%)")

    # Step 4: Merge with existing results.json
    print("💾 Saving to results.json...")
    try:
        # Load existing results if present
        existing_results = []
        if os.path.exists('results.json'):
            with open('results.json', 'r', encoding='utf-8') as f:
                existing_results = json.load(f)
                if not isinstance(existing_results, list):
                    existing_results = []
        
        # Create a map by ps_id for merging
        existing_by_id = {r.get('ps_id'): r for r in existing_results if isinstance(r, dict) and r.get('ps_id')}
        
        # Add new records (they will overwrite if ps_id already exists)
        for record in server_records:
            ps_id = record.get('ps_id')
            if ps_id:
                existing_by_id[ps_id] = record
        
        # Convert back to list and save
        final_results = list(existing_by_id.values())
        
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(final_results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully saved {len(final_results)} total problems to results.json")
        print(f"   📊 {len(server_records)} new problems added")
        print(f"   📊 {len(existing_results)} existing problems")
        
        return final_results
        
    except Exception as e:
        print(f"❌ Error saving results: {e}")
        return server_records


def main():
    """Main function to run the complete pipeline."""
    # Check if API key is set
    if not GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY environment variable not set!")
        print("Please set it with: set GEMINI_API_KEY=your_api_key_here")
        print("Get your API key from: https://aistudio.google.com/app/apikey")
        return
    
    try:
        results = run_pipeline()
        if results:
            print(f"\n🎉 Pipeline completed successfully!")
            print(f"📊 Total problems in results.json: {len(results)}")
            
            # Show a sample of the latest additions
            latest = [r for r in results if r.get('ps_id', '').startswith('25')]
            if latest:
                print(f"📋 Latest problem: {latest[-1].get('ps_id')} - {latest[-1].get('title', '')[:60]}...")
        else:
            print(f"\n✨ All caught up! No new problems to process.")
            
    except KeyboardInterrupt:
        print("\n⏹️  Pipeline interrupted by user")
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()