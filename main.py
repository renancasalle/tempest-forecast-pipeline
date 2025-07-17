import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO
from dotenv import load_dotenv

def main():
    
    load_dotenv() 

    api_key = os.getenv('API_KEY')
    base_path = os.getenv('FILE_PATH')

    if not api_key:
        print("api_key not found")
        return
    
    initial_date = datetime.today()
    final_date = initial_date + timedelta(days=7)
    city = 'London'

    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{initial_date.strftime("%Y-%m-%d")}/{final_date.strftime("%Y-%m-%d")}?unitGroup=metric&include=days&key={api_key}&contentType=csv'

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        df = pd.read_csv(StringIO(response.text))

        folder_name = initial_date.strftime('%Y-%m-%d')
        file_path = os.path.join(base_path, folder_name)

        os.makedirs(file_path, exist_ok=True)

        df.to_csv(os.path.join(file_path, 'dados_brutos.csv'), index=False)
        df[['datetime', 'tempmin', 'tempmax', 'temp']].to_csv(os.path.join(file_path, 'temperaturas.csv'), index=False)
        df[['datetime', 'description', 'icon']].to_csv(os.path.join(file_path, 'condicoes.csv'), index=False)
        
    except requests.exceptions.RequestException as e:
        print(f"request error: {e}")

if __name__ == "__main__":
    main()
