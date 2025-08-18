# AI Usage & Data Policy Web Crawler

A Python-based pipeline that crawls websites, detects AI and data policy keywords, aggregates results and exposes them through a Streamlit dashboard.

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   playwright install
   ```
4. Download the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the pipeline
Add root URLs to `data/urls_to_crawl.txt` (one per line).

Run the full pipeline:
```bash
python main.py
```
Run individual stages:
```bash
python main.py --crawl       # crawl only
python main.py --analyze     # analyze only
python main.py --aggregate   # aggregate only
```
Launch the Streamlit interface:
```bash
streamlit run src/frontend/app.py
```

## Testing
Run the test suite and record results:
```bash
./run_tests.sh
```
This script appends the timestamp and pass/fail status to `logs/test_log.txt`.

You may also run tests directly:
```bash
pytest
```
