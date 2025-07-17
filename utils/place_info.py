import os
from langchain_tavily import TavilySearch
from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper
from dotenv import load_dotenv

load_dotenv() 

class GooglePlaceSearchTool:
    def __init__(self, api_key: str):
        self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=api_key)
        self.places_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)
    
    def google_search_attractions(self, place: str) -> dict:
        """
        Searches for attractions in the specified place using GooglePlaces API.
        """
        return self.places_tool.run(f"top attractive places in and around {place}")
    
    def google_search_restaurants(self, place: str) -> dict:
        """
        Searches for available restaurants in the specified place using GooglePlaces API.
        """
        return self.places_tool.run(f"what are the top 10 restaurants and eateries in and around {place}?")
    
    def google_search_activity(self, place: str) -> dict:
        """
        Searches for popular activities in the specified place using GooglePlaces API.
        """
        return self.places_tool.run(f"Activities in and around {place}")

    def google_search_transportation(self, place: str) -> dict:
        """
        Searches for available modes of transportation in the specified place using GooglePlaces API.
        """
        return self.places_tool.run(f"What are the different modes of transportations available in {place}")

class TavilyPlaceSearchTool:
    def __init__(self):
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.has_tavily = self.tavily_api_key and self.tavily_api_key != "your_tavily_api_key_here"

    def tavily_search_attractions(self, place: str) -> str:
        """
        Searches for attractions in the specified place using TavilySearch.
        """
        if not self.has_tavily:
            return f"Unable to search for attractions in {place} - API service unavailable. Please visit local tourism websites for information."
        
        try:
            tavily_tool = TavilySearch(api_key=self.tavily_api_key, topic="general", include_answer="advanced")
            result = tavily_tool.invoke({"query": f"top attractive places in and around {place}"})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return str(result)
        except Exception as e:
            return f"Unable to search for attractions in {place} - service error: {str(e)}"
    
    def tavily_search_restaurants(self, place: str) -> str:
        """
        Searches for available restaurants in the specified place using TavilySearch.
        """
        if not self.has_tavily:
            return f"Unable to search for restaurants in {place} - API service unavailable. Please check local restaurant review websites."
        
        try:
            tavily_tool = TavilySearch(api_key=self.tavily_api_key, topic="general", include_answer="advanced")
            result = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}."})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return str(result)
        except Exception as e:
            return f"Unable to search for restaurants in {place} - service error: {str(e)}"
    
    def tavily_search_activity(self, place: str) -> str:
        """
        Searches for popular activities in the specified place using TavilySearch.
        """
        if not self.has_tavily:
            return f"Unable to search for activities in {place} - API service unavailable. Please check local tourism websites."
        
        try:
            tavily_tool = TavilySearch(api_key=self.tavily_api_key, topic="general", include_answer="advanced")
            result = tavily_tool.invoke({"query": f"activities in and around {place}"})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return str(result)
        except Exception as e:
            return f"Unable to search for activities in {place} - service error: {str(e)}"

    def tavily_search_transportation(self, place: str) -> str:
        """
        Searches for available modes of transportation in the specified place using TavilySearch.
        """
        if not self.has_tavily:
            return f"Unable to search for transportation in {place} - API service unavailable. Please check local transport authority websites."
        
        try:
            tavily_tool = TavilySearch(api_key=self.tavily_api_key, topic="general", include_answer="advanced")
            result = tavily_tool.invoke({"query": f"What are the different modes of transportations available in {place}"})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return str(result)
        except Exception as e:
            return f"Unable to search for transportation in {place} - service error: {str(e)}"
    