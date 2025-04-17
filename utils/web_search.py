# At the beginning of the file
import os
import sys
import re
import traceback
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import WEBDRIVER_TIMEOUT, LINK_LOAD_TIMEOUT, CHROMEDRIVER_PATH
from utils.cache_utils import get_from_cache, add_to_cache

# Modified function with local import
def get_search_results_with_cache(query: str) -> dict:
    """Checks semantic cache using FAISS. If miss, performs live search and caches."""
    print(f"\n[get_search_results_with_cache] Received query: '{query}'")
    
    if not query or not isinstance(query, str):
        print("   ⚠️ Invalid query received. Returning error.", file=sys.stderr)
        return {"error": "Invalid or empty query received.", "_cache_status": "Error"}
    
    query = query.strip()
    if not query:
         print("   ⚠️ Empty query after stripping. Returning error.", file=sys.stderr)
         return {"error": "Empty query received.", "_cache_status": "Error"}

    # Local import to avoid circular dependency
    from utils.embedding_utils import get_embedding
    
    # Generate embedding for the query
    query_vector = get_embedding(query, task_type="RETRIEVAL_QUERY")
    if query_vector is None:
        print("   ⚠️ Embedding failed. Skipping cache lookup. Performing live search.")
        live_data = _perform_web_search_and_extract(query)
        live_data["_cache_status"] = "Live Search (Embedding Failed)"
        return live_data

    # Try to get from cache
    cached_data, similarity_score = get_from_cache(query, query_vector)
    if cached_data is not None:
        print(f"[get_search_results_with_cache] Cache HIT with similarity {similarity_score:.4f}. Returning cached result.")
        return cached_data

    # Cache miss, perform live search
    print(f"[get_search_results_with_cache] Cache MISS. Performing live search.")
    live_data = _perform_web_search_and_extract(query)
    
    # Cache the result if it's valid
    if isinstance(live_data, dict) and "error" not in live_data and live_data:
        add_to_cache(query, query_vector, live_data)
        live_data["_cache_status"] = "Live Search (Cache Miss)"
    elif isinstance(live_data, dict) and "error" in live_data:
        live_data["_cache_status"] = f"Live Search Failed ({live_data.get('error', 'Unknown error')})"
    else:
        if not isinstance(live_data, dict): 
            live_data = {"error": "Live search returned non-dict data.", "_cache_status": "Live Search Failed (Internal Error)"}
        elif not live_data: 
            live_data = {"error": "Live search returned empty results.", "_cache_status": "Live Search Failed (Empty)"}
    
    print("[get_search_results_with_cache] Returning live search result.")
    return live_data
