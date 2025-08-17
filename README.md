AI Usage & Data Policy Web Crawler
A Python-based solution to crawl organizational websites, detect AI usage, and extract related data usage policies. The findings are presented in a filterable, multi-page web interface with AI-powered search and shareable, URL-based filters.

Features
Authenticated Crawling: Uses Playwright to crawl websites that require login (including SharePoint) via a one-time manual authentication.

Incremental Updates: Only crawls new or modified pages on subsequent runs to save time and resources.

AI & Policy Detection: Scans page content to identify mentions of Artificial Intelligence and data usage policies.

Interactive Dashboard: A web interface built with Streamlit to display and filter the aggregated results.

Shareable Filters: Filter settings on the dashboard are saved to the URL, allowing users to bookmark and share specific views.

AI-Powered Search: A natural language search bar that uses a generative AI model to answer questions about the crawled content and provide hyperlinked sources.

Collapsible Site Map: A tree-view of all crawled sites and pages, with controls to expand and collapse the hierarchy.

Project Structure
.
├── app.py                  # Main Streamlit application entry point
├── config/
│   └── settings.yaml       # Configuration for crawler (e.g., depth, user-agent)
├── data/
│   ├── urls_to_crawl.txt   # List of root URLs to crawl
│   ├── crawled_data.jsonl  # Raw output from the crawler
│   ├── analysis_results.json # Output from the analysis module
│   └── ai_policy_report.csv  # Final aggregated data for the dashboard
├── pages/
│   ├── 1_Dashboard.py      # Streamlit page for the main dashboard
│   ├── 2_AI_Search.py      # Streamlit page for the AI search feature
│   └── 3_Site_Map.py       # Streamlit page for the site map view
├── src/
│   ├── crawler/
│   │   ├── auth_handler.py
│   │   ├── state_manager.py
│   │   └── spider.py
│   ├── analyzer/
│   │   └── detector.py
│   └── aggregator.py
├── tests/
│   ├── test_analyzer.py    # Pytests for the analysis module
│   └── test_aggregator.py  # Pytests for the aggregator module
├── main.py                 # Main runner script to orchestrate the pipeline
├── requirements.txt        # Python dependencies
└── README.md               # This file

Setup and Installation
Clone the repository:

git clone <your-repository-url>
cd <your-repository-name>

Create and activate a Python virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required dependencies:

pip install -r requirements.txt

Install the necessary Playwright browsers:

playwright install

Download the spaCy language model:

python -m spacy download en_core_web_sm

Configuration
Add URLs to Crawl: Open the data/urls_to_crawl.txt file and add the root URLs you wish to crawl, with one URL per line.

Manual Authentication (First-Time Setup): The crawler needs an authenticated session to access private sites like SharePoint.

The first time you run the crawler, it will open a browser window.

Manually log in to all necessary websites (e.g., your organization's SharePoint, Duke's single sign-on).

Once you are logged in, the crawler will save the session information to a user profile. Subsequent runs will use this profile to run without manual login.

How to Run
The application is run from the command line using main.py.

Run the full pipeline (Crawl and Analyze):

python main.py --crawl

Run only the analysis (if crawling is already done):

python main.py --analyze

Launch the Web Application:

streamlit run app.py

Testing
This project uses pytest for testing. You can run all tests from the root directory.

pytest

Tests are located in the tests/ directory and use mock data to ensure functionality without requiring network access or API keys.

Using the Application
After launching the Streamlit app, you can navigate between the different pages using the sidebar:

AI Policy Dashboard: The main view for your data. You can:

Filter the table using the controls on the sidebar.

See your filter selections reflected in the browser's URL.

Copy and share the URL to send a pre-filtered view to others.

AI Search: Ask natural language questions about the crawled content. The AI will respond with an answer and include hyperlinks to the source pages it used.

Site Map: Explore a complete, hierarchical tree of every page that was discovered during the crawl. You can expand and collapse sections to navigate the site structures.
