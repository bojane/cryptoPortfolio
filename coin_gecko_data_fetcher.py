import requests
import csv
import os
import pandas as pd
from config import COINGECKO_API_KEY
import time
import datetime



def get_crypto_price(coin):
    api_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}&x_cg_demo_api_key={COINGECKO_API_KEY}"

    try:
        response = requests.get(api_url)
        retry_delay = 0.2  # initial delay in seconds


        while response.status_code == 429:
            print("Throttled. Retrying after delay.")
            time.sleep(retry_delay)
            retry_delay *= 2  # exponential backoff
            response = requests.get(api_url)

        if response.status_code != 200:
            return f"Failed to retrieve data. Status code: {response.status_code}, response: {response.text}"


        
        
        
        if 'application/json' in response.headers['Content-Type']:
            data = response.json()
            
            if data:
                crypto_data = data[0]
                current_price = crypto_data.get('current_price', 'N/A')
                market_cap = crypto_data.get('market_cap', 'N/A')
                if current_price is None or not isinstance(current_price, (int, float)):
                    return 0.0,0.0  # Return 0.0 if current price is not available or not numeric
                #print(current_price)
                print(f'current_price {current_price} type: {type(current_price)}')
                return current_price, market_cap

        else:
            return f"Unexpected response format: {response.headers['Content-Type']}"


    except json.JSONDecodeError:
        return f"JSON parsing error, response was: {response.text}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}, Response: {response.text if 'response' in locals() else 'No response'}"


def get_crypto_data(coins):
    coin_ids = ','.join(coins)
    api_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin_ids}&x_cg_demo_api_key={COINGECKO_API_KEY}"

    try:
        response = requests.get(api_url)
        retry_delay = 0.2  # initial delay in seconds

        while response.status_code == 429:
            print("Throttled. Retrying after delay.")
            time.sleep(retry_delay)
            retry_delay *= 2  # exponential backoff
            response = requests.get(api_url)

        if response.status_code != 200:
            return f"Failed to retrieve data. Status code: {response.status_code}, response: {response.text}"

        if 'application/json' in response.headers['Content-Type']:
            data = response.json()
            
            crypto_data = {}
            for coin in data:
                coin_id = coin['id']
                current_price = coin.get('current_price', 0.0)
                market_cap = coin.get('market_cap', 'N/A')
                crypto_data[coin_id] = {'current_price': current_price, 'market_cap': market_cap}
            
            return crypto_data

        else:
            return f"Unexpected response format: {response.headers['Content-Type']}"

    except json.JSONDecodeError:
        return f"JSON parsing error, response was: {response.text}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}, Response: {response.text if 'response' in locals() else 'No response'}"

def calculate_portfolio_value(portfolio, current_prices):
    total_value = 0
    for crypto, data in portfolio.items():
        amount = data['Amount']
        price_when_bought = data.get('Price When Bought')

        current_price = current_prices.get(crypto, 'N/A')
        if current_price != 'N/A' and price_when_bought is not None:
            try:
                current_price = float(current_price)
                price_when_bought = float(price_when_bought)

                value = current_price * amount
                percentage_gain = ((current_price - price_when_bought) / price_when_bought) * 100
                total_value += value

            except ValueError:
                current_price = 'N/A'
                price_when_bought = 'N/A'
                percentage_gain = 'N/A'
        else:
            total_value += 0
            current_price = 'N/A'
            price_when_bought = 'N/A'
            percentage_gain = 'N/A'

        data = {
            "Crypto": [crypto.capitalize()],
            "Price When Bought": [f"${price_when_bought:.2f}" if price_when_bought != 'N/A' else 'N/A'],
            "Current Price": [f"${current_price:.2f}" if current_price != 'N/A' else 'N/A'],
            "Amount": [amount],
            "Total Value": [f"${value:.2f}"],
            "Percentage Gain": [f"{percentage_gain:.2f}%" if percentage_gain != 'N/A' else 'N/A']
        }

        df = pd.DataFrame(data)

        # Append DataFrame to an existing HTML file (if it exists) or create a new one
        with open('crypto_portfolio.html', 'a' if os.path.exists('crypto_portfolio.html') else 'w') as f:
            df.to_html(f, index=False, header=not os.path.exists('crypto_portfolio.html'))

    return total_value


def read_portfolio_csv(filename):
    crypto_portfolio = {}
    stable_portfolio = {}
    all_coins = set()

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            crypto_type = row['Type'].strip().lower()
            crypto = row['Crypto'].strip().lower()
            amount = float(row['Amount']) if row.get('Amount') else 0.0
            price_when_bought = float(row['Price When Bought']) if row.get('Price When Bought') else None
            date_bought = row['Date Bought']
            comments = row['Comments']

            if crypto_type == "crypto":
                crypto_portfolio[crypto] = {'Amount': amount, 'Price When Bought': price_when_bought, 'Date Bought': date_bought, 'Comments': comments}
            elif crypto_type == "stable":
                stable_portfolio[crypto] = {'Amount': amount, 'Price When Bought': price_when_bought, 'Date Bought': date_bought, 'Comments': comments}

            all_coins.add(crypto)

    crypto_data = get_crypto_data(list(all_coins))
    
    current_prices = {coin: data['current_price'] for coin, data in crypto_data.items()}
    market_caps = {coin: data['market_cap'] for coin, data in crypto_data.items()}

    return crypto_portfolio, stable_portfolio, current_prices, market_caps

def portfolio_to_dataframe(portfolio, current_prices, market_caps):
    rows = []

    # First, we ensure that all prices are numeric, and replace any non-numeric data with 0.0
    numeric_current_prices = {name: (price if isinstance(price, (int, float)) else 0.0) for name, price in current_prices.items()}

    # Calculate the total portfolio value for later use in calculating the percentage of portfolio
    total_value = sum(amount['Amount'] * numeric_current_prices[name] for name, amount in portfolio.items())

    for name, data in portfolio.items():
        #print(f'name: \ {name} \n data: \n {data} \n')
        current_price = numeric_current_prices.get(name, 0.0)
        market_cap = market_caps.get(name, 'N/A')  # Get market cap for each crypto

        price_when_bought = data['Price When Bought']
        amount = data['Amount']
        date_bought = data['Date Bought']
        
        total_value_coin = amount * current_price
        percentage_gain = ((current_price - price_when_bought) / price_when_bought * 100) if price_when_bought else None
        percentage_of_portfolio = (total_value_coin / total_value * 100) if total_value > 0 else 0
        Comments = data['Comments']

        rows.append({
            'Name': name,
            'Amount': amount,
            'Current Price': current_price,
            'Price When Bought': price_when_bought,
            'Date Bought': date_bought,
            'Percentage Gain': round(percentage_gain,1),
            'Total Value (USD)': round(total_value_coin,1),
            'Percentage of Portfolio': round(percentage_of_portfolio, 2),
            'Market Cap': market_cap,
            'Comments' : Comments,
        })

    df = pd.DataFrame(rows)
    # Sort the DataFrame by 'Percentage of Portfolio' in descending order
    df = df.sort_values(by='Percentage of Portfolio', ascending=False)

    df['Index Nr'] = range(1, len(df) + 1)

    df['Market Cap'] = df['Market Cap'].round(3)

    return df

def calculate_totals_and_percentages(stable_portfolio, crypto_portfolio, current_prices):
    # Initialize totals
    total_stable = 0.0
    total_crypto = 0.0

    # Sum up total amounts for stablecoins and cryptocurrencies
    for name, data in stable_portfolio.items():
        total_stable += data['Amount'] * current_prices.get(name, 0.0)
    for name, data in crypto_portfolio.items():
        #print(f"Name: {name}, Amount: {data['Amount']}, Type of Amount: {type(data['Amount'])}, Current Price: {current_prices.get(name, 0.0)}, Type of Current Price: {type(current_prices.get(name, 0.0))}")
        total_crypto += data['Amount'] * current_prices.get(name, 0.0)

    # Calculate the total value of the entire portfolio
    total_portfolio = total_stable + total_crypto

    # Avoid division by zero in case the portfolio is empty
    if total_portfolio > 0:
        stable_percentage = (total_stable / total_portfolio) * 100
        crypto_percentage = (total_crypto / total_portfolio) * 100
    else:
        stable_percentage = 0.0
        crypto_percentage = 0.0

    # Create a dictionary for DataFrame
    data = {
        'Stable Amount': [round(total_stable,0)],
        'Crypto Amount': [round(total_crypto,0)],
        'Total Amount': [total_portfolio],  # Add the total combined value here
        'Stable Percentage': [round(stable_percentage,1)],
        'Crypto Percentage': [round(crypto_percentage,1)]
    }

    # Create DataFrame
    df_totals = pd.DataFrame(data)
    return df_totals


if __name__ == "__main__":
    #crypto_portfolio, stable_portfolio, current_prices = read_portfolio_csv('crypto_portfolio.csv')
    #crypto_df = portfolio_to_dataframe(crypto_portfolio,current_prices)
    #print(crypto_df)
    #stable_df = portfolio_to_dataframe(stable_portfolio,current_prices)
    crypto_portfolio, stable_portfolio, current_prices, market_caps = read_portfolio_csv('crypto_portfolio.csv')  # Unpack the market_caps
    crypto_df = portfolio_to_dataframe(crypto_portfolio, current_prices, market_caps)
    stable_df = portfolio_to_dataframe(stable_portfolio, current_prices, market_caps)
    # ... [rest of your main function code] ...

    #print(stable_df)

    df_totals = calculate_totals_and_percentages(stable_portfolio, crypto_portfolio, current_prices)

    

    print(df_totals)

    

    html_string = '''
    <html>
    <head><title>Crypto Portfolio Overview</title></head>
    <body>
        <h2>Report Generated on: {current_date_time}</h2>

        <!-- Buttons for Update and Current actions -->
        <form action="/update" method="post">
        <input type="submit" value="Update">
        </form>
        <form action="/current" method="post">
        <input type="submit" value="Current">
        </form>

        <h1>Crypto Portfolio</h1>
        {crypto_table}
        <h1>Stable Portfolio</h1>
        {stable_table}
        <h1>Portfolio Totals</h1>
        {totals_table}
    </body>
    </html>
    '''

# Use the .to_html() function to convert dataframes to HTML tables
# Escape=False allows for characters like '<' and '>' to be rendered properly (use with caution)
crypto_html = crypto_df.to_html(escape=False, index=False)
stable_html = stable_df.to_html(escape=False, index=False)
totals_html = df_totals.to_html(escape=False, index=False)

# Get the current date and time
current_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Use the format function to insert the tables and the current date/time into the html_string
complete_html = html_string.format(current_date_time=current_date_time, crypto_table=crypto_html, stable_table=stable_html, totals_table=totals_html)

# Write the HTML to a file
with open('portfolio_overview.html', 'w') as f:
    f.write(complete_html)