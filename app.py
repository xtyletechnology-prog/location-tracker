from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

app = Flask(__name__)

# Retrieve the API key from environment variables
API_KEY = os.getenv('NUMVERIFY_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    location_info = None
    error = None
    if request.method == 'POST':
        phone_number = request.form.get('phone')
        if phone_number:
            url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={phone_number}"
            response = requests.get(url)
            data = response.json()
            if data['valid']:
                location_info = {
                    'country': data.get('country_name'),
                    'carrier': data.get('carrier'),
                    'location': data.get('location'),
                    'line_type': data.get('line_type')
                }
            else:
                error = "Invalid phone number."
        else:
            error = "Please enter a phone number."
    return render_template('index.html', location_info=location_info, error=error)

if __name__ == '__main__':
    app.run(debug=True)