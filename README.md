# AI Usage & Data Policy Web Crawler

A Python-based pipeline that crawls websites, detects AI and data policy keywords, aggregates results, and exposes them through a Streamlit dashboard.

## Quick Start 🚀

This section provides the fastest way for a developer to get the project up and running.

1. **Clone the repository:**
  
  ```
  git clone https://github.com/sagearbor/dcriCrawl.gitcd dcriCrawl
  ```
  
2. **Create and activate a virtual environment:**
  
  ```
  python3 -m venv venvsource venv/bin/activate  # On macOS/Linux# For Windows: venv\Scripts\activate
  ```
  
3. **Install dependencies:**
  
  ```
  pip install -r requirements.txt
  ```
  
4. **Install Playwright browsers with system dependencies:**
  
  ```
  playwright install --with-deps
  ```
  
  - **Why the `--with-deps` flag?** This ensures that all required system dependencies (like libraries for web rendering) are installed, which is crucial for Playwright to function correctly.
5. **Download the spaCy model:**
  
  ```
  python -m spacy download en_core_web_sm
  ```
  
  - **Why Playwright?** This command downloads the necessary web browsers (Chromium, Firefox, and WebKit) that **Playwright** uses to perform the web crawling. It's a required one-time setup step for the web scraper.
    
  - **Why spaCy?** This command downloads a pre-trained small English language model (`en_core_web_sm`) that **spaCy** uses for natural language processing (NLP). The model is essential for the `analyze` stage of the pipeline to detect policy keywords.
    

## Running the Pipeline

Before running, add the root URLs you wish to crawl to `data/urls_to_crawl.txt`, one URL per line.

- **Run the full pipeline (Crawl, Analyze, Aggregate):**
  
  ```
  python main.py
  ```
  
- **Run individual stages:**
  
  ```
  python main.py --crawl      # crawls websites and saves raw datapython main.py --analyze    # analyzes saved data for policy keywordspython main.py --aggregate  # aggregates and summarizes analysis results
  ```
  
- **Launch the Streamlit dashboard:**
  
  ```
  streamlit run src/frontend/app.py
  ```
  
  The dashboard will open in your web browser.
  

## Testing

- **Run the full test suite:**
  
  ```
  pytest
  ```
  
- **Run the provided test script:**
  
  ```
  ./run_tests.sh
  ```
  
  *Note: This script requires executable permissions. If it fails, run `chmod +x run_tests.sh` first.*
