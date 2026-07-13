from ddgs import DDGS
import time

class WebSearchTool:
    def __init__(self):
        # No API keys required. We are scraping directly.
        pass

    def search(self, query: str) -> str:
        """Executes a live web search via DuckDuckGo and formats the output."""
        try:
            # We add a 2-second sleep so DuckDuckGo doesn't rate-limit our IP
            time.sleep(2) 
            
            # Fetch top 5 results
            results = DDGS().text(query, max_results=5)
            
            if not results:
                return ""
            
            # Synthesize the search results into a clean context block for Claude/Gemini
            search_context = ""
            for res in results:
                search_context += f"Title: {res.get('title', 'N/A')}\n"
                search_context += f"Snippet: {res.get('body', 'N/A')}\n"
                search_context += f"URL: {res.get('href', 'N/A')}\n\n"
                
            return search_context
            
        except Exception as e:
            print(f"Warning: Web Search failed - {e}")
            return ""