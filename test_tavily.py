from tavily import TavilyClient
import os
api_key = "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"
print(f"Testing Tavily API Key: {api_key[:5]}...")
try:
    client = TavilyClient(api_key=api_key)
    response = client.search("What is the latest news about Tesla?", search_depth="basic")
    print("\nSuccess! Search Results:")
    for result in response['results'][:2]:
        print(f"- {result['title']}: {result['url']}")
except Exception as e:
    print(f"\nError testing Tavily: {e}")