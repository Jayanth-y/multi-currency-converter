
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import List

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any frontend
    allow_methods=["*"],  # Allow all request types (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
    allow_credentials=True
)

# Your API key goes here
API_KEY = "<your-key-here>"

# API Key for fetching exchange rates
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

@app.get("/convert/")
def convert_currency(base_currency: str, amount: float, target_currencies: List[str] = Query(...)):
    try:
        # Fetch exchange rates for the base currency
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
                one_target_to_base = 1 / conversion_rates[currency]  # 1 target = how much base
                one_base_to_target = conversion_rates[currency]      # 1 base = how much target
                
                result[currency] = {
                    "converted_amount": round(converted_value, 2),
                    "one_target_to_base": round(one_target_to_base, 4),
                    "one_base_to_target": round(one_base_to_target, 4)
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