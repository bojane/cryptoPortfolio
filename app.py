from flask import Flask, send_file, request, Response, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import subprocess

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": "password",  # Secure password storage is recommended
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def homepage():
    # Serve the HTML file
    return send_file('portfolio_overview.html')

@app.route('/update', methods=['POST'])
@auth.login_required
def update_data():
    # Run your script to update the HTML file
    subprocess.run(['python', 'coin_gecko_data_fetcher.py'], check=True)
    # Redirect to the homepage to display updated data
    return redirect(url_for('homepage'))

@app.route('/current', methods=['POST'])
@auth.login_required
def current_data():
    # Redirect to the homepage without updating
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)