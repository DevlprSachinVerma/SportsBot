# SportsBot
Streamlit Sports Chatbot powered by Google Gemini (gemini-2.0-flash). Features live web scraping (Selenium) for recent info &amp; FAISS semantic caching.
# Streamlit Sports Chatbot with Gemini, Selenium & FAISS Cache



## Overview

This project implements an interactive **Sports Information Chatbot** using Python and Streamlit. It leverages the power of Google's **Gemini large language model (`gemini-2.0-flash`)** to understand user queries and generate informative responses about various sports topics. For up-to-date information like live scores or recent commentary, it employs **Selenium** for web scraping, with results optimized through a **FAISS**-based semantic cache using Google's embedding models.

The primary goal is to provide accurate sports information, using internal knowledge first and resorting to live web data only when necessary or explicitly requested (e.g., for commentary).

## Features

*   **Conversational AI:** Utilizes Google Gemini (`gemini-2.0-flash`) for natural language understanding and response generation regarding sports rules, history, players, stats, etc.
*   **Live Web Search:** Integrates a tool using **Selenium** and **BeautifulSoup4** to scrape Bing search results and linked pages. This is crucial for:
    *   Fetching live scores or results from the last ~3 days.
    *   Finding specific textual **commentary** or play-by-play descriptions when requested.
*   **Semantic Caching:** Implements a robust caching layer to minimize redundant web searches and API calls:
    *   Uses Google's `embedding-001` model to create vector embeddings of search queries.
    *   Stores embeddings and references to cached results in a **FAISS** index (`faiss-cpu`) for efficient similarity searching.
    *   If a similar query is found above a defined threshold (`CACHE_SIMILARITY_THRESHOLD`), cached results are served instantly.
    *   Raw scraped data is stored locally in JSON files within the cache directory.
*   **Streamlit User Interface:** Provides a clean, interactive chat interface built with Streamlit for easy user interaction.
*   **Tool-Augmented Generation:** Follows a pattern where the LLM can decide to use external tools (the web search cache function) to augment its knowledge.
*   **Local Execution Focus:** Primarily configured and documented for running on a local machine, requiring specific setup for Selenium.

## Technology Stack

*   **Frontend:** Streamlit
*   **LLM:** Google Gemini (`gemini-2.0-flash` via `google-generativeai` SDK)
*   **Embeddings:** Google Embedding Model (`embedding-001`)
*   **Web Scraping:** Selenium, BeautifulSoup4, lxml
*   **Vector Search/Caching:** FAISS (`faiss-cpu`), NumPy
*   **Configuration (Local):** `python-dotenv`, `.streamlit/secrets.toml`
*   **Core:** Python 3.9+

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1.  **Python:** Version 3.9 or higher recommended. (`python --version`)
2.  **Git:** For cloning the repository. (`git --version`)
3.  **Visual Studio Code (Recommended):** Or any other code editor/IDE.
4.  **VS Code Python Extension:** If using VS Code.
5.  **Google API Key:** An active API key for Google AI Studio (Gemini).
    *   Obtain from [Google AI Studio](https://aistudio.google.com/).
    *   **Keep this key secure!**
6.  **Google Chrome Browser:** Selenium requires a browser installation.
7.  **ChromeDriver:** The WebDriver executable matching your **exact** Chrome version.
    *   Check Chrome Version: `chrome://settings/help`
    *   Download ChromeDriver: [Chrome for Testing availability dashboard](https://googlechromelabs.github.io/chrome-for-testing/)
    *   **Placement:**
        *   **Recommended:** Add the directory containing the `chromedriver` executable to your system's **PATH** environment variable.
        *   **Alternative:** Modify the `CHROMEDRIVER_PATH` variable near the top of `streamlit_app.py` to the *full, absolute path* of the executable (e.g., `CHROMEDRIVER_PATH = "/path/to/your/chromedriver"` or `C:\\path\\to\\your\\chromedriver.exe`). If set to `None` (default), it checks the PATH.

## Local Setup Instructions (Using VS Code)

1.  **Clone Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory-name>
    ```

2.  **Open in VS Code:**
    ```bash
    code .
    ```

3.  **Create & Activate Virtual Environment:** (Highly Recommended)
    Open the VS Code integrated terminal (`Ctrl+` or `Cmd+`).
    ```bash
    # Create environment
    python -m venv .venv

    # Activate environment
    # Windows (Git Bash/PowerShell):
    source .venv/Scripts/activate
    # macOS/Linux:
    source .venv/bin/activate
    ```
    Your terminal prompt should now show `(.venv)`.

4.  **Select Python Interpreter (VS Code):**
    *   Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
    *   Type `Python: Select Interpreter`.
    *   Choose the Python interpreter located within your `.venv` directory (it might be marked 'Recommended').

5.  **Install Dependencies:**
    Ensure the virtual environment is active. Install all required packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    *(Make sure the `requirements.txt` file provided in the previous step exists in your project root.)*

## Configuration

### 1. Google API Key (Secrets)

For local execution that mimics Streamlit Cloud's secret handling (`st.secrets`), create a local secrets file:

1.  **Create Directory:** In your project's root directory, create `.streamlit`:
    ```bash
    mkdir .streamlit
    ```
2.  **Create File:** Inside `.streamlit`, create `secrets.toml`.
3.  **Add Key:** Open `secrets.toml` and add your key:
    ```toml
    # .streamlit/secrets.toml
    GOOGLE_API_KEY = "YOUR_ACTUAL_GOOGLE_API_KEY_GOES_HERE"
    ```
    *(Replace with your real key. Do not add extra quotes around the key string itself.)*
4.  **Ignore Secrets:** **Crucially**, ensure the `.streamlit` directory is added to your `.gitignore` file to prevent committing secrets:
    ```gitignore
    # .gitignore
    .venv/
    __pycache__/
    *.pyc
    .streamlit/  # IMPORTANT! Prevents committing secrets
    search_cache_v6_text_commentary/
    *.DS_Store
    .env # If using the alternative .env method
    ```

*(**Alternative:** You could use a `.env` file with `python-dotenv`. If you do, create `.env` in the root, add `GOOGLE_API_KEY="YOUR_KEY"`, ensure `load_dotenv()` is called early in the script, add `.env` to `.gitignore`, and potentially modify the script's key retrieval logic if `st.secrets` doesn't find the key.)*

### 2. ChromeDriver

Ensure ChromeDriver is correctly installed and accessible either via your system's PATH or by setting the `CHROMEDRIVER_PATH` variable directly in `streamlit_app.py`, as described in the **Prerequisites**.

## Running the Application

1.  **Activate Virtual Environment:** If not already active:
    ```bash
    # Windows:
    source .venv/Scripts/activate
    # macOS/Linux:
    source .venv/bin/activate
    ```
2.  **Run Streamlit:** From the project root directory in your terminal:
    ```bash
    streamlit run streamlit_app.py
    ```
3.  Streamlit will start the server and automatically open the application in your default web browser.

## How It Works (Simplified Flow)

1.  **User Input:** The user types a question into the Streamlit chat interface.
2.  **Initial LLM Check:** The query is sent to the Gemini model via the `google-generativeai` SDK. The model first attempts to answer using its internal knowledge based on the system instructions.
3.  **Tool Decision:** If the query requires recent information (live scores, commentary) or if the model lacks confidence, it may decide to call the `get_search_results_with_cache` tool.
4.  **Embedding & Cache Check:**
    *   An embedding vector is generated for the query using `embedding-001`.
    *   The FAISS index is searched for similar query embeddings.
5.  **Cache Hit:** If a similar query is found above the threshold, the corresponding cached JSON data (previously scraped results) is retrieved from the `search_cache_v6_text_commentary/` directory.
6.  **Cache Miss (Live Search):**
    *   If no suitable cache entry exists, the `_perform_web_search_and_extract` function is called.
    *   Selenium launches a headless Chrome instance, navigates to Bing, searches, and scrapes the results page.
    *   It then visits the top relevant links, scraping their content using BeautifulSoup.
    *   The extracted text data is structured into a dictionary.
7.  **Cache Update:** If the live search was successful, the results dictionary is saved as a JSON file, and the query embedding + file path are added to the FAISS index and mapping file. `faiss.write_index` saves the updated index.
8.  **Response Synthesis:** The Gemini model receives the information (either from internal knowledge, cached data, or fresh scraped data) and synthesizes the final response. For commentary requests using scraped data, it aims to rephrase the information in an engaging style.
9.  **Display:** The final response is displayed in the Streamlit chat interface.

## Cache Management

*   All cache files related to web search results are stored in the `search_cache_v6_text_commentary/` directory.
*   `faiss_index_v6.idx`: The FAISS index file containing query embeddings.
*   `faiss_mapping_v6.json`: A JSON file mapping FAISS index IDs to the original query and the path to the cached JSON result file. It also stores the next available ID.
*   `*.json`: Individual JSON files (named by a hash of the query) containing the scraped data for each unique query performed live.
*   **Clearing the Cache:** To completely reset the web search cache, simply delete the entire `search_cache_v6_text_commentary/` directory. It will be automatically recreated on the next run when a web search is needed.

## Troubleshooting

*   **`selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH...`**: ChromeDriver is not found or incompatible. Verify installation, version match with Chrome, and PATH configuration or the `CHROMEDRIVER_PATH` variable in the script.
*   **`KeyError: 'GOOGLE_API_KEY'`**: API key is missing or incorrect. Ensure `.streamlit/secrets.toml` exists, is correctly formatted, contains the right key name (`GOOGLE_API_KEY`), and is saved. Also, ensure `.streamlit` is *not* listed in `.gitignore` if you expect it to be tracked (though typically secrets shouldn't be).
*   **`ModuleNotFoundError: No module named 'X'`**: A required Python package is missing. Activate your virtual environment (`.venv`) and run `pip install -r requirements.txt`.
*   **Selenium Errors (Timeout, Element Not Found, etc.):** Web scraping is inherently fragile. Bing or target websites might change their structure, breaking the selectors used in `_perform_web_search_and_extract`. The script might need updates to the scraping logic. Websites may also employ anti-scraping measures.
*   **High Resource Usage:** Running Selenium (a full browser) and FAISS can consume significant RAM and CPU, especially during indexing or scraping.
*   **Cache Inconsistency Errors:** If the app crashes during a cache write, the index and mapping files *might* become inconsistent. Deleting the cache directory usually resolves this.

## Limitations & Known Issues

*   **Selenium Dependency:** Requires a specific browser (Chrome) and matching WebDriver (ChromeDriver) setup, making deployment to platforms without browser environments (like standard Streamlit Community Cloud) difficult without modification (see Future Improvements).
*   **Scraping Fragility:** Web scraping logic can easily break if website layouts change.
*   **Potential for Blocks:** Automated scraping can be detected and blocked by websites or search engines.
*   **Resource Intensive:** Selenium can be heavy on system resources.
*   **Cache Persistence:** The file-based cache works well locally but is ephemeral on platforms like Streamlit Cloud unless external storage is configured.
*   **Accuracy:** Relies on the accuracy of both the Gemini model and the scraped web content, which may not always be perfect or up-to-date.
*   **Commentary Synthesis:** The quality of synthesized commentary depends heavily on the quality and relevance of the text found during scraping.

## Future Improvements

*   **Replace Selenium:** Implement web search using official Search Engine APIs (Google Custom Search API, Bing Search API) or third-party scraping APIs (SerpApi, ScraperAPI) for increased robustness and easier deployment.
*   **Automated WebDriver Management:** Integrate `webdriver-manager` to automatically download and manage the correct ChromeDriver version.
*   **Error Handling:** Enhance error handling during scraping and API calls.
*   **Cache Invalidation:** Implement a strategy for expiring or refreshing cached items (e.g., time-based invalidation for recent results).
*   **UI Enhancements:** Add features like displaying cache status, source links for web results, or progress indicators during scraping.
*   **Alternative Vector Stores:** Explore cloud-based vector databases for persistent caching if deploying.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests. (Add contribution guidelines if desired).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (Create a LICENSE file, e.g., containing the standard MIT License text).
