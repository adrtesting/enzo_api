import requests
import uuid
import os
from dotenv import load_dotenv



load_dotenv(override=True)
SECRET_KEY = os.getenv("SECRET_KEY")
API_URL = os.getenv("API_URL")  

print(f"Loaded SECRET_KEY: {SECRET_KEY}")
print(f"Loaded API_URL: {API_URL}")

def make_request():
    headers = {
        "Authorization": f"Bearer {SECRET_KEY}",  
        "Content-Type": "application/json", 
        "CallTreeId": str(uuid.uuid4()),    
    }

    payload = {
        "store":"724",
        "fulfillmentType":"FSD",
        "articles":[ {"mgb": "82408001002"}
        ]
    }

    try:
        
        response = requests.get(API_URL, headers=headers, json=payload)

       
        if response.status_code == 200:
            print("Request successful!")
            print(response.json())  
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)  
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    make_request()
