# Crypto Portfolio Tracker

A Flask-based web application that tracks and displays your cryptocurrency portfolio. This app fetches real-time data from the CoinGecko API, calculates portfolio values, and presents the information in an easy-to-read HTML format.

## Features

- Fetches real-time cryptocurrency data from CoinGecko API
- Displays purchase value and current value for each cryptocurrency
- Calculates and shows percentage gain/loss for each holding
- Presents data in a matrix format for both crypto and stablecoin holdings
- Provides a summary of total portfolio value and distribution
- Secure access with basic HTTP authentication
- Ability to update data on demand

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/bojane/cryptoPortfolio.git
   ```

2. Navigate to the project directory:
   ```
   cd cryptoPortfolio
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `config.py` file in the root directory with your CoinGecko API key:
   ```python
   COINGECKO_API_KEY = 'your_api_key_here'
   ```

2. Update the `crypto_portfolio.csv` file with your cryptocurrency holdings. The CSV should have the following columns:
   - Type (crypto or stable)
   - Crypto (cryptocurrency name)
   - Amount
   - Price When Bought
   - Date Bought
   - Comments

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your web browser and go to `http://localhost:5000`

3. Log in with the credentials set in `app.py`

4. You will see a matrix displaying your cryptocurrency holdings, their purchase values, and current performance in percentage.

5. Use the "Update" button to fetch the latest data from CoinGecko

6. Use the "Current" button to view the most recently fetched data without making a new API call

## Files

- `app.py`: Flask application that serves the web interface
- `coin_gecko_data_fetcher.py`: Script that fetches data from CoinGecko and generates the HTML report
- `crypto_portfolio.csv`: CSV file containing your cryptocurrency holdings
- `portfolio_overview.html`: Generated HTML file displaying your portfolio

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/bojane/cryptoPortfolio/issues).

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

Your Name - bjorkmanders@protonmail.com

Project Link: [https://github.com/bojane/cryptoPortfolio](https://github.com/bojane/cryptoPortfolio)
