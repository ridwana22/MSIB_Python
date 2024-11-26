from fastapi import FastAPI, HTTPException, Query
import requests
import uvicorn

app = FastAPI()

BASE_URL = "https://api.exchangerate-api.com/v4/latest/"

@app.get("/convert_rate/")
def tukar(
    base_currency: str = Query(..., description="Kode mata uang asal (contoh: USD, IDR)"),
    target_currency: str = Query(..., description="Kode mata uang tujuan (contoh: EUR, IDR)"),
):
    try:
        # Membuat URL dengan base_currency
        url = f"{BASE_URL}{base_currency}"
        response = requests.get(url)

        # Jika API memberikan respons yang buruk
        response.raise_for_status()

        # Mengambil data JSON
        data = response.json()

        # Validasi respons dari API
        if "rates" not in data or target_currency not in data["rates"]:
            raise HTTPException(status_code=400, detail="Invalid target currency or missing rates in response")

        return {
            "base_currency": base_currency,
            "target_currency": target_currency,
            "exchange_rate": data["rates"][target_currency],
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error fetching exchange rates: {e}")
    except KeyError:
        raise HTTPException(status_code=500, detail="Unexpected response format from API.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8500)
