#currency convertor Tool

from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper
from langchain.tools import tool
from dotenv import load_dotenv
from typing import List
import os

class BasicCalculator:
    """Basic calculator for expense calculations"""
    def multiply(self, a: float, b: float) -> float:
        return float(a) * float(b)
    
    def calculate_total(self, *costs: float) -> float:
        return sum(float(cost) for cost in costs)
    
    def calculate_daily_budget(self, total_cost: float, days: int) -> float:
        return float(total_cost) / int(days)

class CurrencyCalculator:
    def __init__(self):
        load_dotenv()
        self.calculator = BasicCalculator()  # Initialize calculator
        self.currency_calculator_tools_list = self.setup_tools()
        
    def setup_tools(self) -> List:
        
        """Setup all tools for the currency conversion, expense calculation & Hotel cost estimations """

        @tool
        def currency_convertor(from_currency:str ,to_currency:str , value: float):
            """
            Convert currency from one type to another using Alpha Vantage API.
            
            Args:
                from_currency (str): The source currency code (e.g., 'USD', 'EUR')
                to_currency (str): The target currency code (e.g., 'USD', 'EUR')
                value (float): The amount to convert
            
            Returns:
                float: The converted currency value
            """
            try:
                convertor = AlphaVantageAPIWrapper(alphavantage_api_key=os.getenv("ALPHAVANTAGE_API_KEY"))
                response = convertor._get_exchange_rate(from_currency, to_currency)
                
                exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
                
                return float(value) * float(exchange_rate)
            except Exception as e:
                print(f"Currency conversion error: {e}")
                return float(value)  # Return original value if conversion fails

        @tool
        def estimate_total_hotel_cost(price_per_night: float, total_days: float) -> float:
            """Calculate total hotel cost"""
            return self.calculator.multiply(price_per_night, total_days)
        
        @tool
        def calculate_total_expense(*costs: float) -> float:
            """Calculate total expense of the trip"""
            return self.calculator.calculate_total(*costs)
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            return self.calculator.calculate_daily_budget(total_cost, days)
        
        return [currency_convertor,estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]
        