import io
import pandas as pd
import requests


def get_nse_stock_list():
    # Official archive URL for the complete list of listed equities
    url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"

    # Set up browser headers to prevent the server from blocking the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    try:
        # Establish a session to persist headers/cookies
        session = requests.Session()
        session.headers.update(headers)

        # Fetch the CSV data
        print("Fetching stock list from NSE...")
        response = session.get(url, timeout=15)
        response.raise_for_status()

        # Read the CSV content bytes into a pandas DataFrame
        df = pd.read_csv(io.BytesIO(response.content))

        # Clean up column names by removing extra spaces
        df.columns = df.columns.str.strip()

        print(f"Successfully retrieved {len(df)} listed stocks.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


# --- Run the function ---
if __name__ == "__main__":
    stocks_df = get_nse_stock_list()

    if stocks_df is not None:
        # Display the first 5 stocks
        print("\n--- Preview of the Stock List ---")
        print(stocks_df[["SYMBOL", "NAME OF COMPANY", "SERIES"]].head())

        # Optional: Save to a local CSV file
        # stocks_df.to_csv("nse_stocks.csv", index=False)
