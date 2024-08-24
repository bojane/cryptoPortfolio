# Update cryptocurrency data using coin_gecko_data_fetcher.py
import subprocess

def update_crypto_data():
    try:
        subprocess.run(['python', 'coin_gecko_data_fetcher.py'], check=True)
        return True
    except Exception as e:
        print(f"Error updating cryptocurrency data: {str(e)}")
        return False