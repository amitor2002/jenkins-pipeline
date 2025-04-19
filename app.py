from flask import Flask, render_template, request
from services.weather_service import get_weather_data, get_coordinates

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """Handle the home page requests."""
    if request.method == 'POST':
        city = request.form.get('city')
        country = request.form.get('country')

        if not city and not country:
            error_message = "Please enter at least a city or country name"
            return render_template('index.html', error_message=error_message)

        latitude, longitude, country, city = get_coordinates(city, country)

        if latitude is None or longitude is None:
            error_message = "Location not found. Try again."
            return render_template('index.html', error_message=error_message)

        data = get_weather_data(latitude, longitude)

        if data:
            temperature_today = data.get('temperature_today', 'N/A')
            humidity_today = data.get('humidity_today', 'N/A')
            temperature_today_morning = data.get('temp today morning', 'N/A')
            temperature_today_evening = data.get('temp today evening', 'N/A')
            humidity_today_morning = data.get('humid today morning', 'N/A')
            humidity_today_evening = data.get('humid today evening', 'N/A')
            weekly_forecast = data.get('weekly_forecast', [])
        else:
            temperature_today = 'Data not available'
            humidity_today = 'Data unknown'
            temperature_today_morning = 'N/A'
            temperature_today_evening = 'N/A'
            humidity_today_morning = 'N/A'
            humidity_today_evening = 'N/A'
            weekly_forecast = []

        return render_template(
            'index.html',
            temperature_today=temperature_today,
            humidity_today=humidity_today,
            temperature_today_morning=temperature_today_morning,
            temperature_today_evening=temperature_today_evening,
            humidity_today_morning=humidity_today_morning,
            humidity_today_evening=humidity_today_evening,
            weekly_forecast=weekly_forecast,
            city=city,
            country=country
        )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)