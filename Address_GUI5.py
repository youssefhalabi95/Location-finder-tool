import urllib.request
import urllib.parse
import json
import tkinter as tk
import threading
import webbrowser

current_lat = None
current_lon = None

# API URL
serviceurl = "https://py4e-data.dr-chuck.net/opengeo?"

# Function that runs when button is clicked
def get_coordinates():
    address = entry.get().strip()

    if not address:
        result_label.config(text="⚠️ Please enter a location")
        return

    result_label.config(text="⏳ Loading...")

    # Run the real work in a thread
    threading.Thread(target=fetch_data, args=(address,)).start()

def fetch_data(address):
    params = {'q': address}
    url = serviceurl + urllib.parse.urlencode(params)

    try:
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        js = json.loads(data)

        if not js or 'features' not in js or len(js['features']) == 0:
            result_label.config(text="❌ Location not found")
            return

        lat = js['features'][0]['properties']['lat']
        lon = js['features'][0]['properties']['lon']
        location = js['features'][0]['properties']['formatted']

        global current_lat, current_lon
        current_lat = lat
        current_lon = lon

        result_label.config(
            text=f"✅ Location: {location}\nLatitude: {lat}\nLongitude: {lon}"
        )

        save_to_history(location, lat, lon)

    except:
        result_label.config(text="❌ Error: Check your internet or try again")

def save_to_history(location, lat, lon):
    with open("history.txt", "a") as f:
        f.write(f"{location} | {lat}, {lon}\n")

def open_map():
    if current_lat and current_lon:
        webbrowser.open(f"https://www.google.com/maps?q={current_lat},{current_lon}")
    else:
        result_label.config(text="⚠️ No location to open yet")

# Create window
window = tk.Tk()
window.title("Location Finder")
window.geometry("400x200")

# Input field
entry = tk.Entry(window, width=40)
entry.pack(pady=10)

# Button
button = tk.Button(window, text="Get Coordinates", command=get_coordinates)
button.pack(pady=5)

# Output label
result_label = tk.Label(window, text="", justify="left")
result_label.pack(pady=10)

map_button = tk.Button(window, text="Open in Google Maps", command=open_map)
map_button.pack(pady=5)

# Run the app
window.mainloop()