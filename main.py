import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO
from dotenv import load_dotenv

def main():
    
    load_dotenv() 

    api_key = os.getenv('API_KEY')

    if not api_key:
        print("API_KEY not found. Please set it in your environment variables.")
        return
    
    initial_date = datetime.today()
    final_date = initial_date + timedelta(days=7)
    city = 'London'

    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{initial_date.strftime("%Y-%m-%d")}/{final_date.strftime("%Y-%m-%d")}?unitGroup=metric&include=days&key={api_key}&contentType=csv'

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        df = pd.read_csv(StringIO(response.text))
        file_path = f'{initial_date.strftime("%Y-%m-%d")}_a_{final_date.strftime("%Y-%m-%d")}.csv'
        df.to_csv(file_path, index=False)
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

if __name__ == "__main__":
    main()
