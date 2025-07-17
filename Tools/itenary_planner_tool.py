import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from langchain.tools import tool
from dotenv import load_dotenv

class ItineraryPlannerTool:
    def __init__(self):
        load_dotenv()
        self.itinerary_tool_list = self._setup_tools()
    
    def _setup_tools(self) -> List:
        """Setup all tools for the itinerary planner"""
        
        @tool
        def create_daily_itinerary(destination: str, activities: str, duration_days: int, budget_range: str = "medium") -> str:
            """Create a detailed daily itinerary for a destination.
            Args:
                destination: The travel destination
                activities: Comma-separated list of preferred activities
                duration_days: Number of days for the trip
                budget_range: Budget range (low, medium, high)
            """
            try:
                # Parse activities
                activity_list = [activity.strip() for activity in activities.split(',')]
                
                # Create itinerary structure
                itinerary = {
                    "destination": destination,
                    "duration": f"{duration_days} days",
                    "budget_range": budget_range,
                    "activities": activity_list,
                    "daily_plan": []
                }
                
                # Generate daily plans
                for day in range(1, duration_days + 1):
                    daily_plan = {
                        "day": day,
                        "title": f"Day {day} in {destination}",
                        "morning": "Morning activities to be planned based on preferences",
                        "afternoon": "Afternoon activities to be planned",
                        "evening": "Evening activities and dining",
                        "accommodation": "Hotel/accommodation suggestions",
                        "transport": "Transportation recommendations",
                        "budget_estimate": "Daily budget estimate based on range"
                    }
                    itinerary["daily_plan"].append(daily_plan)
                
                # Format response
                response = f"""
## 🗓️ {duration_days}-Day Itinerary for {destination}

**Budget Range:** {budget_range.title()}
**Preferred Activities:** {', '.join(activity_list)}

"""
                
                for day_plan in itinerary["daily_plan"]:
                    response += f"""
### {day_plan['title']}

🌅 **Morning:**
- {day_plan['morning']}

🌞 **Afternoon:**
- {day_plan['afternoon']}

🌙 **Evening:**
- {day_plan['evening']}

🏨 **Accommodation:**
- {day_plan['accommodation']}

🚗 **Transportation:**
- {day_plan['transport']}

💰 **Budget Estimate:**
- {day_plan['budget_estimate']}

---
"""
                
                return response
                
            except Exception as e:
                return f"Error creating itinerary: {str(e)}"
        
        @tool
        def optimize_itinerary_by_location(attractions: str, city: str) -> str:
            """Optimize itinerary by grouping attractions by location/area in the city.
            Args:
                attractions: Comma-separated list of attractions to visit
                city: The city name for location optimization
            """
            try:
                attraction_list = [attraction.strip() for attraction in attractions.split(',')]
                
                # Create location-based grouping (simplified example)
                optimized_plan = f"""
## 📍 Location-Optimized Itinerary for {city}

### Attractions to Visit:
{', '.join(attraction_list)}

### Optimized Route Suggestions:

**Zone 1 - City Center/Downtown:**
- Group nearby attractions in the city center
- Recommended duration: Half day
- Transportation: Walking or public transport

**Zone 2 - Cultural District:**
- Museums, galleries, and cultural sites
- Recommended duration: Full day
- Transportation: Public transport or taxi

**Zone 3 - Recreational Areas:**
- Parks, outdoor activities, and scenic spots
- Recommended duration: Half to full day
- Transportation: May require private transport

### Travel Tips:
- Start early to maximize time at each location
- Book tickets in advance for popular attractions
- Check opening hours and days
- Consider purchasing city tourist passes for discounts

### Estimated Timeline:
- Allow 2-3 hours per major attraction
- Include travel time between zones (30-60 minutes)
- Factor in meal breaks and rest periods
"""
                
                return optimized_plan
                
            except Exception as e:
                return f"Error optimizing itinerary: {str(e)}"
        
        @tool
        def create_budget_breakdown(destination: str, duration_days: int, traveler_count: int, budget_category: str = "medium") -> str:
            """Create a detailed budget breakdown for the trip.
            Args:
                destination: Travel destination
                duration_days: Number of days
                traveler_count: Number of travelers
                budget_category: Budget category (low, medium, high)
            """
            try:
                # Budget multipliers based on category
                multipliers = {
                    "low": {"accommodation": 50, "food": 30, "transport": 20, "activities": 25},
                    "medium": {"accommodation": 100, "food": 60, "transport": 40, "activities": 50},
                    "high": {"accommodation": 200, "food": 120, "transport": 80, "activities": 100}
                }
                
                base_costs = multipliers.get(budget_category, multipliers["medium"])
                
                # Calculate costs
                accommodation_total = base_costs["accommodation"] * duration_days
                food_total = base_costs["food"] * duration_days * traveler_count
                transport_total = base_costs["transport"] * traveler_count
                activities_total = base_costs["activities"] * duration_days * traveler_count
                
                total_budget = accommodation_total + food_total + transport_total + activities_total
                per_person_budget = total_budget / traveler_count if traveler_count > 0 else total_budget
                
                budget_breakdown = f"""
## 💰 Budget Breakdown for {destination}

**Trip Details:**
- Destination: {destination}
- Duration: {duration_days} days
- Travelers: {traveler_count} person(s)
- Budget Category: {budget_category.title()}

### Cost Breakdown:

🏨 **Accommodation:**
- ${base_costs['accommodation']}/night × {duration_days} nights = ${accommodation_total}

🍽️ **Food & Dining:**
- ${base_costs['food']}/person/day × {traveler_count} travelers × {duration_days} days = ${food_total}

🚗 **Transportation:**
- ${base_costs['transport']}/person = ${transport_total}

🎯 **Activities & Attractions:**
- ${base_costs['activities']}/person/day × {traveler_count} travelers × {duration_days} days = ${activities_total}

### Summary:
- **Total Budget:** ${total_budget}
- **Per Person:** ${per_person_budget:.2f}
- **Daily Average:** ${total_budget/duration_days:.2f}

### Budget Tips:
- Book accommodations in advance for better rates
- Look for local restaurants for authentic and affordable meals
- Consider city tourist passes for activity discounts
- Use public transportation when possible
- Set aside 10-15% extra for unexpected expenses

*Note: Prices are estimates and may vary based on season, availability, and specific choices.*
"""
                
                return budget_breakdown
                
            except Exception as e:
                return f"Error creating budget breakdown: {str(e)}"
        
        @tool
        def create_travel_checklist(destination: str, duration_days: int, travel_season: str = "general") -> str:
            """Create a comprehensive travel checklist for the trip.
            Args:
                destination: Travel destination
                duration_days: Number of days
                travel_season: Season of travel (spring, summer, fall, winter, general)
            """
            try:
                checklist = f"""
## ✅ Travel Checklist for {destination}

**Trip Duration:** {duration_days} days
**Season:** {travel_season.title()}

### 📋 Pre-Travel Planning (2-4 weeks before):
- [ ] Book flights and accommodation
- [ ] Check passport validity (6+ months remaining)
- [ ] Apply for visa if required
- [ ] Purchase travel insurance
- [ ] Notify bank of travel plans
- [ ] Research local customs and etiquette
- [ ] Check vaccination requirements
- [ ] Download offline maps and translation apps
- [ ] Book popular attractions in advance

### 🧳 Packing Essentials:

**Documents:**
- [ ] Passport/ID
- [ ] Travel insurance documents
- [ ] Flight tickets and hotel confirmations
- [ ] Emergency contact information
- [ ] Copies of important documents (stored separately)

**Electronics:**
- [ ] Phone and charger
- [ ] Portable power bank
- [ ] Universal adapter
- [ ] Camera
- [ ] Headphones

**Clothing ({travel_season} appropriate):**
- [ ] Comfortable walking shoes
- [ ] Weather-appropriate clothing
- [ ] Sleepwear
- [ ] Underwear and socks
- [ ] Light jacket or sweater
- [ ] Formal outfit (if needed)

**Health & Personal Care:**
- [ ] Prescription medications
- [ ] First aid kit
- [ ] Sunscreen
- [ ] Personal hygiene items
- [ ] Hand sanitizer
- [ ] Face masks

**Money & Cards:**
- [ ] Local currency
- [ ] Credit/debit cards
- [ ] Emergency cash in USD/EUR
- [ ] Money belt or secure wallet

### 📱 Day Before Departure:
- [ ] Check flight status
- [ ] Complete online check-in
- [ ] Pack carry-on essentials
- [ ] Charge all devices
- [ ] Confirm transportation to airport
- [ ] Check weather forecast
- [ ] Review first day itinerary

### 🌍 Upon Arrival:
- [ ] Get local SIM card or activate roaming
- [ ] Exchange money if needed
- [ ] Download local transportation apps
- [ ] Save emergency numbers
- [ ] Inform family/friends of safe arrival

### 🏠 Before Returning:
- [ ] Check souvenirs for customs restrictions
- [ ] Confirm return flight details
- [ ] Pack souvenirs securely
- [ ] Clear accommodation charges
- [ ] Rate and review accommodations

*Customize this checklist based on your specific destination and travel style.*
"""
                
                return checklist
                
            except Exception as e:
                return f"Error creating travel checklist: {str(e)}"
        
        # Return all the tools
        return [create_daily_itinerary, create_travel_checklist]

