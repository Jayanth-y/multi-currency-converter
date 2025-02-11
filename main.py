import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import List

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API Key from Environment Variable
API_KEY = os.getenv("EXCHANGE_API_KEY")
if not API_KEY:
    raise ValueError("API Key not found. Please set EXCHANGE_API_KEY.")

BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

@app.get("/convert/")
def convert_currency(
    base_currency: str,
    amount: float,
    target_currencies: List[str] = Query(...)
):
    try:
        # Fetch exchange rates
        response = requests.get(BASE_URL + base_currency)
        data = response.json()

        # Handle API errors
        if "error" in data:
            raise HTTPException(status_code=400, detail="Invalid API Key or Currency Code")

        conversion_rates = data.get("conversion_rates", {})
        result = {}

        for currency in target_currencies:
            if currency in conversion_rates:
                converted_value = amount * conversion_rates[currency]
                one_target_to_base = 1 / conversion_rates[currency]  
                one_base_to_target = conversion_rates[currency]      
                
                result[currency] = {
                    "converted_amount": round(converted_value, 2),
                    "one_target_to_base": round(one_target_to_base, 6),
                    "one_base_to_target": round(one_base_to_target, 6)
                }
            else:
                result[currency] = "Currency not available"

        return {
            "base_currency": base_currency,
            "amount": amount,
            "converted_values": result
        }

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="API Request Failed")
