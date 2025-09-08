# SIH Problem Classification Pipeline

A simple automated pipeline that scrapes new SIH problem statements, classifies them using Gemini AI, and saves them to `results.json`.

## Setup

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Set your Gemini API key:**
   ```
   set GEMINI_API_KEY=your_api_key_here
   ```
   Get your API key from: https://aistudio.google.com/app/apikey

## Usage

### Option 1: Run directly
```
python server.py
```

### Option 2: Use the batch file (Windows)
```
run_daily.bat
```

## What it does

1. 🔎 **Scrapes** new problem statements from https://sih.gov.in/sih2025PS
2. 🧠 **Classifies** them using Gemini Flash Lite (30 problems per minute)
3. 💾 **Saves** results to `results.json` with complete data including:
   - Problem details (title, description, organization, etc.)
   - AI-generated summary and tags
   - Submission count
   - Classification metadata

## Output Format

Each problem in `results.json` looks like:
```json
{
  "ps_id": "SIH25001",
  "title": "Smart Community Health Monitoring...",
  "summary": "Develop a Smart Health Surveillance...",
  "description": "Problem Statement...",
  "difficulty": ["Med"],
  "technology": ["AI", "IoT"],
  "stakeholders": ["Government Agencies"],
  "impact_area": ["Safety"],
  "data_resource_type": ["Sensor Data"],
  "solution_type": "Mobile and Web Solutions",
  "organization": "Ministry of Development...",
  "department": "Ministry of Health...",
  "category": "Software",
  "theme": "MedTech / BioTech / HealthTech",
  "submission_count": 0
}
```

## Performance

- **~150 problems** processed in **~5 minutes**
- **Incremental updates** - only processes new problems
- **Automatic retry** for failed classifications
- **Rate limit compliant** with Gemini API

## Scheduling

To run this daily automatically, you can:

1. **Windows Task Scheduler**: Schedule `run_daily.bat` to run once per day
2. **Cron (Linux/Mac)**: Add to crontab: `0 2 * * * cd /path/to/backend && python server.py`

## Files

- `server.py` - Main pipeline script
- `scraper.py` - Web scraping utilities
- `results.json` - Output file with all classified problems
- `scraper_state.json` - Tracks last processed problem ID
- `requirements.txt` - Python dependencies
- `run_daily.bat` - Windows batch runner
