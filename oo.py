import requests
import tkinter as tk
from tkinter import messagebox

# Function to get weather data from OpenWeatherMap API
def get_weather(city):
    api_key = 'e3775eac13580044f5e16ba4f8433ce6'  # Replace with your OpenWeatherMap API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    
    try:
        # Send GET request to OpenWeatherMap API
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for bad status codes
        data = response.json()
        
        # Check if the response contains the expected data
        if data.get("cod") != 200:
            return {"error": data.get("message", "Error retrieving weather data.")}
        
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching weather data: {e}"}

# Function to assess the safety of traveling based on weather conditions
def assess_safety(city):
    weather_data = get_weather(city)
    
    if "error" in weather_data:
        return weather_data['error']
    
    # Extract weather information
    weather_condition = weather_data.get('weather', [{}])[0].get('main', '')
    temperature = weather_data.get('main', {}).get('temp', 0) - 273.15  # Convert from Kelvin to Celsius
    temperature_fahrenheit = (temperature * 9/5) + 32  # Convert to Fahrenheit for easier interpretation

    # Print weather condition and temperature for reference
    print(f"Weather Condition: {weather_condition}")
    print(f"Temperature: {temperature:.2f}°C ({temperature_fahrenheit:.2f}°F)")
    
    # Define safety thresholds based on weather conditions
    warnings = []
    safe_message = "The weather looks good for travel."
    
    # Check for severe weather conditions and extreme temperatures
    if weather_condition in ['Thunderstorm', 'Drizzle', 'Rain', 'Snow', 'Squall', 'Tornado']:
        warnings.append("Warning: Severe weather conditions detected. It's not safe to travel.")
        safe_message = "Due to severe weather conditions, it's not recommended to travel."
    
    if temperature < 0:
        warnings.append("Warning: Freezing temperatures detected. Travel might be hazardous.")
        safe_message = "Freezing temperatures detected. It's not recommended to travel."
    
    if temperature > 35:
        warnings.append("Warning: Extremely high temperatures detected. Travel may be dangerous.")
        safe_message = "Extremely high temperatures detected. Avoid travel if possible."
    
    if weather_condition == 'Clear':
        safe_message = "Weather is clear. Safe for travel!"
    
    if weather_condition == 'Clouds' and 20 <= temperature <= 30:
        safe_message = "Mild weather with clouds. Travel is safe."
    
    # Return travel safety evaluation
    if warnings:
        return "\n".join(warnings)
    
    return safe_message

# Function to display the result in the UI
def display_result():
    city = city_entry.get()
    result = assess_safety(city)
    messagebox.showinfo("Travel Safety Status", result)

# Create the main UI window
root = tk.Tk()
root.title("Travel Safety Checker")

# Create a label and entry box
city_label = tk.Label(root, text="Enter City Name:")
city_label.pack()
city_entry = tk.Entry(root)
city_entry.pack()

# Create a button to check safety
check_button = tk.Button(root, text="Check Safety", command=display_result)
check_button.pack()

# Run the Tkinter event loop
root.mainloop()
