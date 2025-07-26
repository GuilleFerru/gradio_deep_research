"""
Test script for SearchManager without using Gradio
"""
import asyncio
from src.search_manager import SearchManager
from dotenv import load_dotenv

async def test_search_manager():
    # Load environment variables
    load_dotenv(override=True)
    
    # Create a test query
    test_query = "Latest AI Agent frameworks in 2025"
    print(f"Running search with query: '{test_query}'")
    
    # Create SearchManager instance and run search
    search_manager = SearchManager()
    result = await search_manager.run(test_query)
    
    # Print the result
    print("\nSearch Results:")
    print("=" * 50)
    print(result)
    print("=" * 50)

if __name__ == "__main__":
    # Run the test function
    asyncio.run(test_search_manager())
