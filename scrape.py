import json
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import time

# Initialize the geocoder to find GPS coordinates
geolocator = Nominatim(user_agent="latvia_water_map_bot")

# The HTML snippet you provided (If you were fetching this live, you'd use requests.get() here)
html_data = """
<div class="sidebar-fixed-area svelte-1xo6bpy"><div slot="fixed"><div><h1>Amata, Melturi</h1></div></div></div>
<div class="content" key="Amata, Melturi">
    <p>Dati par 04.03.2026 07:50</p> 
    <p>Ūdens līmenis virs stacijas nulles atzīmes: <b>0.69 m</b> </p>
    <p>Ūdens temperatūra: <b>0.9 °C</b> </p>
</div>
"""

soup = BeautifulSoup(html_data, 'html.parser')
scraped_data = []

# 1. Extract the name
name_tag = soup.find('h1')
station_name = name_tag.text.strip() if name_tag else "Unknown Station"

# 2. Extract the water level and temperature from the content div
content_div = soup.find('div', class_='content')
if content_div:
    paragraphs = content_div.find_all('p')
    
    date_time = paragraphs[0].text.strip()
    water_level = "N/A"
    temperature = "N/A"
    
    for p in paragraphs:
        if "Ūdens līmenis virs stacijas nulles atzīmes:" in p.text:
            water_level = p.find('b').text.strip()
        if "Ūdens temperatūra:" in p.text:
            temperature = p.find('b').text.strip()

    # 3. Get GPS Coordinates (adding ", Latvia" to help the search)
    try:
        location = geolocator.geocode(f"{station_name}, Latvia")
        lat = location.latitude if location else 57.0  # Default to central Latvia if not found
        lon = location.longitude if location else 24.0
        time.sleep(1) # Be polite to the geocoding server
    except:
        lat, lon = 57.0, 24.0

    # 4. Save to our dictionary
    station_data = {
        "name": station_name,
        "date": date_time,
        "water_level": water_level,
        "temperature": temperature,
        "lat": lat,
        "lon": lon
    }
    scraped_data.append(station_data)

# 5. Save the data to data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(scraped_data, f, ensure_ascii=False, indent=4)

print("Data scraped and saved to data.json successfully!")
