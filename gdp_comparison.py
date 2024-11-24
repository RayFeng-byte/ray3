import wbdata
import pandas as pd
from datetime import datetime

def get_country_gdp(country_code, start_year, end_year):
    # Define the indicator for GDP (constant 2015 US$)
    indicators = {'NY.GDP.MKTP.KD': 'GDP'}
    # Fetch the data
    data = wbdata.get_dataframe(indicators, country=country_code, date=(f"{start_year}",f"{end_year}"))
    # Clean and format the data
    data = data.reset_index()
    data['date'] = pd.to_datetime(data['date']).dt.year
    data = data.sort_values('date')
    return data
# Example usage:
# gdp_data = get_country_gdp('USA', 2010, 2020)
# print(gdp_data)

from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()
chat = ChatOpenAI(temperature=0)
def get_gdp_data(country_code: str, start_year: int, end_year: int) -> str:
    """Get GDP data for a specific country and time range."""
    data = get_country_gdp(country_code, start_year, end_year)
    return data.to_json()
functions = [
    {
        "name": "get_gdp_data",
        "description": "Get GDP data for a specific country and time range",
        "parameters": {
            "type": "object",
            "properties": {
                "country_code": {
                    "type": "string",
                    "description": "The country code (e.g., 'USA' for United States)"
                },
                "start_year": {
                    "type": "integer",
                    "description": "The start year for the data range"
                },
                "end_year": {
                    "type": "integer",
                    "description": "The end year for the data range"
                }
            },
            "required": ["country_code", "start_year", "end_year"]
        }
    }
]
    
def compare_gdp_growth(country1: str, country2: str, start_year: int, end_year: int) -> str:
    """Compare GDP growth between two countries."""
    messages = [
    HumanMessage(content=f"Compare the GDP growth of {country1} and {country2} from {start_year} to {end_year}."),
    AIMessage(content="Certainly! To compare the GDP growth of these two countries, I'll need to retrieve their GDP data for the specified time range. Let me do that for you."),
    FunctionMessage(name="get_gdp_data", content=get_gdp_data(country1, start_year, end_year)),
    AIMessage(content=f"I've retrieved the GDP data for {country1}. Now, let me get the data for {country2}."),
    FunctionMessage(name="get_gdp_data", content=get_gdp_data(country2, start_year, end_year)),
    AIMessage(content=f"Great, I now have the GDP data for both {country1} and {country2}. I'll analyze this data and provide a comparison of their economic growth."),
    HumanMessage(content="Please provide a detailed analysis comparing the GDP growth of the two countries, including growth rates, trends, and any significant observations.")
    ]
    response = chat(messages)
    return response.content
# Example usage:
# result = compare_gdp_growth('USA', 'CHN', 2010, 2020)
# print(result)

def main():
    print("Welcome to the GDP Growth Comparison Tool!")
    country1 = input("Enter the first country code (e.g., USA): ").upper()
    country2 = input("Enter the second country code (e.g., CHN): ").upper()
    start_year = int(input("Enter the start year: "))
    end_year = int(input("Enter the end year: "))
    print("\nAnalyzing GDP growth...")
    result = compare_gdp_growth(country1, country2, start_year, end_year)
    print("\nAnalysis Results:")
    print(result)
if __name__ == "__main__":
    main()

    