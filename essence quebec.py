
# import data from excel file local to pandas dataframe
import pandas as pd   
import folium
import os 
import webbrowser
from pathlib import Path

# Define output path on Desktop (writable location)
output_dir = Path.home() / "Desktop"
output_file = output_dir / "gazmap.html"

df = pd.read_excel('/Volumes/1TB SSD/VSCODE/pythonproject/_GAZ DATA BASE QUEBEC.xlsx')

# Print column names to identify latitude and longitude columns
print("Columns in the Excel file:")
print(df.columns.tolist())

# Print first few rows to see the data structure
print("\nFirst few rows:")
print(df.head())

# Display latitude and longitude from the dataframe
print("\nLatitude values:")
print(df['Latitude'].tolist())
print("\nLongitude values:")
print(df['Longitude'].tolist())

# Create a map centered on the first location
if len(df) > 0:
    # Use the first row's coordinates as the map center
    center_lat = df['Latitude'].iloc[0]
    center_lon = df['Longitude'].iloc[0]
else:
    center_lat = 45.9729182
    center_lon = -74.1724759

gazmap = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Add markers for each location with company, latitude, and longitude
for idx, row in df.iterrows():
    lat = row['Latitude']
    lon = row['Longitude']
    
    # Skip rows with NaN coordinates
    if pd.isna(lat) or pd.isna(lon):
        continue
    
    company = str(row['Company']).strip() if 'Company' in df.columns else ''
    price = str(row['Price']).strip() if 'Price' in df.columns else ''
    location = str(row['Location']).strip() if 'Location' in df.columns else ''
    
    # Determine color based on price (green <= 130$, orange 130-135$, red > 135$)
    try:
        price_value = float(price.replace("$", "").strip()) if price else 0
        # Green for <= 130$, Orange for 130-135$, Red for > 135$
        if price_value >=139:
            marker_color = "#EE0E0E"  # Red
        elif price_value >=137:
            marker_color = "#FF8C00"  # Orange
        else:
            marker_color = "#50D42F"  # Green
    except:
        marker_color = "#50D42F"  # Default green
    
    # Add popup with company, price, location, latitude, and longitude
    popup_text = f"<b>{company}</b><br>Price: {price}<br>Location: {location}<br>Latitude: {lat}<br>Longitude: {lon}"
    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        tooltip=f"{company} - {price}",
        icon=folium.DivIcon(
            html=f'<div style="font-size: 10pt; color: white; background-color: {marker_color}; padding: 3px 6px; border-radius: 3px; white-space: nowrap;"><b>{company}⛽️</b><br>{price}</div>',
            icon_size=(120, 40),
            icon_anchor=(50, -10),
        )
    #add  a locate me button to the map
    ).add_to(gazmap)


# Save the map to Desktop (writable location)
gazmap.save(str(output_file))
print(f"\nMap saved to {output_file}")

# Automatically open the map in the default browser
webbrowser.open(f"file://{output_file}")
print("Opening map in browser...")

