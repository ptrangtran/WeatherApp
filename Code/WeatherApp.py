import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import requests
from datetime import datetime

#API get weather data
def get_w_data(city):
    #sign in with openweather and get API
    api_key = '' #get api from website
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    
    weather_data = requests.get(url).json()
    forecast_data = requests.get(forecast_url).json()
    
    return weather_data, forecast_data

#function to display weather information
def s_weather():
    city = city_entry.get()
    if city:
        weather_data, forecast_data = get_w_data(city)
      
        #current weather display
        location.config(text=weather_data['name'])
        temperature.config(text=f"{weather_data['main']['temp']}°C")
        weather_description = weather_data['weather'][0]['description'].capitalize()
        weather.config(text=weather_description)
        
        #weather condition matching
        weather_con = weather_data['weather'][0]['main']
       
    
        if 'Clear' in weather_con:
            weather_icon("Clear sky")
        elif 'Clouds' in weather_con:
            weather_icon("Few clouds")
        elif 'Rain' in weather_con:
            weather_icon("Rain")
        elif 'Thunderstorm' in weather_con:
            weather_icon("Thunderstorm")
        elif 'Snow' in weather_con:
            weather_icon("Snow")
        elif 'Mist' in weather_con:
            weather_icon("Mist")
        else:
            weather_icon("Clear sky")
        
        #5-day forecast
        forecast_labels = [day1, day2, day3, day4, day5]
        forecast_days = {}
        for entry in forecast_data['list']:
            date_text = entry['dt_txt']
            date = datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S").date()
            time = datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S").time()
            
            if time.hour == 12:
                forecast_days[date] = entry

        for i, (day, entry) in enumerate(forecast_days.items()):
            if i < 5:
                day_text = f"{day}: {entry['main']['temp']}°C, {entry['weather'][0]['description'].capitalize()}"
                forecast_labels[i].config(text=day_text)
            else:
                break
    else:
        location.config(text="Enter a valid location")

#PM Accelerator info
def show_info():
    info_wind = tk.Toplevel(root)
    info_wind.title("PM Accelerator Info")
    info_wind.geometry("400x200")
    
    info_label = tk.Label(info_wind, text="PM Accelerator: We help tech professionals level up their careers through mentorship, training, and networking opportunities.", wraplength=350)
    info_label.pack(pady=20)

#main window
root = tk.Tk()
root.title("Weather App")
root.minsize(400, 600)

#fonts
font_l = font.Font(family='Helvetica', size=20, weight='bold')
font_m = font.Font(family='Helvetica', size=16)

#enter city and create search button
city_entry = tk.Entry(root, font=font_m)
city_entry.pack(pady=10, fill=tk.X, padx=20)

search_button = tk.Button(root, text="Search", font=font_m, command=s_weather)
search_button.pack(pady=10)

#display location, temp, weather
location = tk.Label(root, font=font_l)
location.pack(pady=10)

temperature = tk.Label(root, font=font_l)
temperature.pack(pady=10)

weather = tk.Label(root, font=font_m)
weather.pack(pady=10)

#PNG icons with conditions
icons_path = "/Users/trang/WeatherApp/icons/"
icons = {
    "Clear sky": ImageTk.PhotoImage(Image.open(icons_path + "Clear sky.png").resize((100, 100))),   
    "Few clouds": ImageTk.PhotoImage(Image.open(icons_path + "Few clouds.png").resize((100, 100))),
    "Rain": ImageTk.PhotoImage(Image.open(icons_path + "Rain.png").resize((100, 100))),
    "Thunderstorm": ImageTk.PhotoImage(Image.open(icons_path + "Thunderstorm.png").resize((100, 100))),
    "Snow": ImageTk.PhotoImage(Image.open(icons_path + "Snow.png").resize((100, 100))),
    "Mist": ImageTk.PhotoImage(Image.open(icons_path + "Mist.png").resize((100, 100))),
}


def weather_icon(condition):
    icon = icons.get(condition, icons["Clear sky"])
    weather_icon_label.config(image=icon)
    weather_icon_label.image = icon

#label weather icon
weather_icon_label = tk.Label(root)
weather_icon_label.pack(pady=10)

#5-day forecast
day1 = tk.Label(root, font=font_m)
day1.pack(pady=5, fill=tk.X)

day2 = tk.Label(root, font=font_m)
day2.pack(pady=5, fill=tk.X)

day3 = tk.Label(root, font=font_m)
day3.pack(pady=5, fill=tk.X)

day4 = tk.Label(root, font=font_m)
day4.pack(pady=5, fill=tk.X)

day5 = tk.Label(root, font=font_m)
day5.pack(pady=5, fill=tk.X)

#display name and info button
b_frame = tk.Frame(root)
b_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

name = tk.Label(b_frame, text="Created by Phuong Trang Tran", font=font_m)
name.pack(side=tk.LEFT, padx=10)

info_but = tk.Button(b_frame, text="Info", font=font_m, command=show_info)
info_but.pack(side=tk.RIGHT, padx=10)

#thinkter main loop
root.mainloop()