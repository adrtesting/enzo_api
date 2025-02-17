import requests
import uuid
import os
import json
import pandas as pd
import time
from dotenv import load_dotenv
# import jwt
# import datetime

# with open(r"C:\Windows\System32\private.rsa", "r") as private_key_file:
#     private_key = private_key_file.read()

# header = {
#     "alg": "RS256",
#     "typ": "JWT",
#     "kid": "K_aa55015a-206a-11ed-98d5-e2cc12b0dc50"
# }
# payload = {
#     "entitlements": "vSPUR",
#     "iat": datetime.datetime.now(datetime.timezone.utc),  
#     "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)  
# }

# token = jwt.encode(payload, private_key, algorithm="RS256", headers=header)

# print(token)

load_dotenv(override=True)
SECRET_KEY = os.getenv("SECRET_KEY")
API_URL = os.getenv("API_URL")  

print(f"Loaded SECRET_KEY: {SECRET_KEY}")
print(f"Loaded API_URL: {API_URL}")

results = []

def make_request(store_id, product_id, customer_segment_id, customer_segment_type, retries=3):
    headers = {
        "JWT": f"{SECRET_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json", 
        "CallTreeId": str(uuid.uuid4()),    
    }

    data = {
    "article": product_id,  
    "store": int(store_id),
    "fulfilmentType": "FSD",
    "customerSegmentType": customer_segment_type,  
    "customerSegmentID": customer_segment_id

    }  

    print("Sending Request with Data", json.dumps(data, indent=2))

    try:
        
        response = requests.post(API_URL, headers=headers, json=data, timeout=10)
        print(f"🔹 Response Status: {response.status_code}")
        print("🔹 Response Content:", response.text)

       
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            
            country_code = response_json.get("country", {}).get("numeric", "N/A")
            store = response_json.get("basket", {}).get("store", "N/A")
            currency = response_json.get("basket", {}).get("currency", "N/A")
            extracted_price = response_json.get("basket", {}).get("price", "N/A")
            errors = [err["error"] for err in response_json.get("errors", [])]

            results.append({
                "store_id": store_id,
                "product_id": product_id,
                "country_code": country_code,
                "customer_segment_id": customer_segment_id,
                "customer_segment_type": customer_segment_type,
                "enzo_price": extracted_price,
                "store": store,
                "currency": currency,
                "errors": errors
            })
            print(f"✅ Extracted Price: {extracted_price} for Store {store_id}, Product {product_id}")

        else:
            print(f"❌ Request failed with status code {response.status_code}") 

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if retries > 0:
            time.sleep(5) 
            make_request(store_id, product_id, customer_segment_id, customer_segment_type, retries - 1)
    else:
        print("Max retries reached. Request failed.")

def process_csv(file_path):
    
    df = pd.read_csv(file_path, dtype={"store_id": str, "product_id": str, "customer_segment_id": str, "customer_segment_type": str})
    print("Processing CSV file with shape:", df.shape)

    for index, row in df.iterrows():
        store_id = row['store_id']
        product_id = row['product_id']
        customer_segment_id = row['customer_segment_id']
        customer_segment_type = row['customer_segment_type']

        make_request(store_id, product_id, customer_segment_id, customer_segment_type)

if __name__ == "__main__":

    csv_file_path = r"C:\APPS\Projects\Price\Enzo\bquxjob_20e9ed45_195134caa6c.csv"
    process_csv(csv_file_path)

    result_df = pd.DataFrame(results)
    result_df.to_csv('enzo_data.csv', index=False)

    print("Results saved to enzo_data.csv")
    
