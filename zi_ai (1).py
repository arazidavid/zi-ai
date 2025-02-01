# -*- coding: utf-8 -*-
"""Zi Ai.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-6TpQIlt6xq57AGfZJqYrYkYR7xB1mNk
"""

!pip install geopandas rasterio tensorflow folium

import geopandas as gpd

# Load your shapefile
data = gpd.read_file('/content/sample_data/Zoning_Py.shp') #when loadind file upload all files in the Zoning py folder

# View the first few rows
print(data.head())

"""All data that is been used is to help run the Ai pending getting data to properly used it for lagos"""

import os
print(os.path.exists('/content/sample_data/Zoning_Py.shp'))

import geopandas as gpd
import matplotlib.pyplot as plt

# Load the shapefile for Prince George's County (replace with actual file path if available)
data = gpd.read_file('/content/sample_data/Zoning_Py.shp') # Ensure the correct file path

# Check the first few rows of the data to confirm it loaded correctly
print(data.head())

# Plot the shapefile
plt.figure(figsize=(10, 10))
data.plot(edgecolor='black', cmap='viridis')
plt.title("Prince George's County Visualization", fontsize=16)
plt.xlabel("Longitude", fontsize=12)
plt.ylabel("Latitude", fontsize=12)
plt.show()

# If you want to save the plot
plt.savefig('/content/PG_County_Visualization.png')

from google.colab import files
files.download('/content/sample_data/Zoning_Py.shp')

from google.colab import files
files.download('/content/sample_data/Zoning_Py.shp')

import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load the dataset
data = gpd.read_file('/content/sample_data/Zoning_Py.shp')

# Encode the CLASS column (e.g., map residential areas to 1, others to 0)
data['CLASS'] = LabelEncoder().fit_transform(data['CLASS'])

# Define features and target
X = data[['ZONE_TYPE', 'SHAPE_AREA', 'SHAPE_LEN']]  # Select relevant feature columns
y = data['CLASS']  # Target column (e.g., encoded as 1 for residential, 0 otherwise)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f'Model Accuracy: {accuracy}')

from sklearn.preprocessing import StandardScaler

# Drop rows with missing values (if any)
data = data.dropna()

# Scale numeric features
scaler = StandardScaler()
data[['SHAPE_AREA', 'SHAPE_LEN']] = scaler.fit_transform(data[['SHAPE_AREA', 'SHAPE_LEN']])

# Verify the data
print(data.head())

# Check unique values in CLASS
print(data['CLASS'].unique())

# Map CLASS to binary
residential_classes = ['Residential', 'Res']  # Update with actual residential labels
data['CLASS'] = data['CLASS'].apply(lambda x: 1 if x in residential_classes else 0)

# Verify mapping
print(data['CLASS'].value_counts())

from sklearn.model_selection import train_test_split

# Define features and target
X = data[['ZONE_TYPE', 'SHAPE_AREA', 'SHAPE_LEN']]
y = data['CLASS']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Verify splits
print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

from sklearn.ensemble import RandomForestClassifier

# Train the Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)

print(f'Training Accuracy: {train_accuracy}')
print(f'Testing Accuracy: {test_accuracy}')

from sklearn.metrics import classification_report, confusion_matrix

# Predictions
y_pred = model.predict(X_test)

# Classification report
print(classification_report(y_test, y_pred))

# Confusion matrix
print(confusion_matrix(y_test, y_pred))

import matplotlib.pyplot as plt

# Add predictions to GeoDataFrame
data['PREDICTION'] = model.predict(X)

# Plot
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
data.plot(column='PREDICTION', ax=ax, legend=True, cmap='coolwarm')
plt.title("Predicted Residential Areas")
plt.show()

# Save as new shapefile
data.to_file('residential_predictions.shp')

# Save as CSV
data[['ZONE_TYPE', 'SHAPE_AREA', 'SHAPE_LEN', 'PREDICTION']].to_csv('residential_predictions.csv', index=False)

!pip install geopandas shapely matplotlib folium

from joblib import dump
dump(model, 'residential_model.pkl')

!ls

from joblib import load

# Load the model file
model = load('residential_model.pkl')

from google.colab import files

# Upload your files
uploaded = files.upload()

!pip install geopandas shapely joblib

import geopandas as gpd
import pandas as pd
from joblib import load
from google.colab import files

# Step 1: Load the trained model
model = load('residential_model.pkl')

# Step 2: Upload and load your spatial data
uploaded = files.upload()  # Upload a GeoJSON or shapefile ZIP
filename = list(uploaded.keys())[0]

if filename.endswith('.zip'):
    data = gpd.read_file(f'zip://{filename}')  # For shapefiles
elif filename.endswith('.geojson'):
    data = gpd.read_file(filename)  # For GeoJSON

# Step 3: Preprocess data (modify as needed)
# Assuming your model expects certain features like "ZONE_TYPE", "SHAPE_AREA", etc.
X = data[['ZONE_TYPE', 'SHAPE_AREA', 'SHAPE_LEN']]

# Step 4: Predict using the model
data['PREDICTION'] = model.predict(X)

# Step 5: Save the results
# Save as GeoJSON
data.to_file('predicted_results.geojson', driver='GeoJSON')

# Save as CSV
data[['ZONE_TYPE', 'SHAPE_AREA', 'SHAPE_LEN', 'PREDICTION']].to_csv('predicted_results.csv', index=False)

print("Predictions saved!")

!pip install streamlit geopandas shapely joblib folium geopy

import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import Point
from joblib import load
from geopy.geocoders import Nominatim

# Load trained model
model = load("residential_model.pkl")

# Load land use dataset
data = gpd.read_file('/content/sample_data/Zoning_Py.shp')  # Update with your dataset

# Streamlit UI
st.title("Zi: AI for Residential Zone Detection")
st.write("Check if your location is in a residential area.")

# Get user location input
latitude = st.number_input("Enter Latitude", value=38.8308, format="%.6f")
longitude = st.number_input("Enter Longitude", value=-76.8661, format="%.6f")

if st.button("Check Location"):
    point = Point(longitude, latitude)
    zone = data[data.contains(point)]

    if not zone.empty:
        st.write("Your location falls in this zone:")
        st.write(zone[['ZONE_TYPE']])  # Modify as needed

        # Predict residential status
        features = zone[['SHAPE_AREA', 'SHAPE_LEN']]
        prediction = model.predict(features)

        if prediction[0] == 1:
            st.success("✅ This is a RESIDENTIAL area.")
        else:
            st.error("❌ This is NOT a residential area.")
    else:
        st.warning("⚠️ No zoning data found for this location.")

    # Map visualization
    m = folium.Map(location=[latitude, longitude], zoom_start=15)
    folium.Marker([latitude, longitude], popup="Your Location", icon=folium.Icon(color="blue")).add_to(m)
    folium_static(m)

!pip install streamlit ngrok
!streamlit run app.py & npx localtunnel --port 8501

!pip install streamlit geopandas shapely joblib folium geopy

# Download GeoJSON
files.download('predicted_results.geojson')

# Download CSV
files.download('predicted_results.csv')

import ipywidgets as widgets
from IPython.display import display

# File upload widget
upload_button = widgets.FileUpload(accept='.geojson,.zip', multiple=False)
display(upload_button)

# Once a file is uploaded, process it
def process_file(change):
    filename = list(upload_button.value.keys())[0]
    with open(filename, 'wb') as f:
        f.write(upload_button.value[filename]['content'])
    print(f"File {filename} saved!")

upload_button.observe(process_file, names='value')

!pip install geopandas shapely joblib geopy

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from joblib import load
from geopy.geocoders import Nominatim

# Load land use shapefile (or GeoJSON)
data = gpd.read_file('/content/sample_data/Zoning_Py.shp')  # Update with your file name

# Check the first few rows
data.head()

# Enter your latitude and longitude manually from Step 1
latitude = 38.954929  # Example: Replace with actual value
longitude = -76.945541  # Example: Replace with actual value

# Convert to a GeoPandas point
point = Point(longitude, latitude)

# Check which zone contains your location
zone = data[data.contains(point)]

if not zone.empty:
    print("Your location is in the following zone:")
    print(zone[['ZONE_TYPE']])
else:
    print("Your location is not in any known zone.")

# Load your trained model
model = load('residential_model.pkl')

# Extract relevant features from the identified zone
if not zone.empty:
    features = zone[['SHAPE_AREA', 'SHAPE_LEN']]  # Adjust column names as needed

    # Predict
    prediction = model.predict(features)

    if prediction[0] == 1:
        print("✅ Your location is in a RESIDENTIAL area.")
    else:
        print("❌ Your location is NOT in a residential area.")
else:
    print("Could not find zoning information for your location.")

!pip install streamlit joblib geopandas shapely folium openai #i want to turn it to a chatbot from here for urban 610

!pip install streamlit_folium

import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import Point
from joblib import load
from streamlit_folium import folium_static
#the code here is to create a chatbot
# Load trained model
model = load("residential_model.pkl")

# Load land use dataset
data = gpd.read_file('/content/sample_data/Zoning_Py.shp')  # Replace with your dataset

# Streamlit chatbot UI
st.title("Zi: Your AI Land Use Assistant")
st.write("Ask about zoning & residential approvals.")

# User input
user_input = st.text_input("Ask Zi something...", "")

if user_input:
    if "residential" in user_input.lower():
        st.write("Please provide your location (latitude, longitude) to check if it's a residential area.")
        latitude = st.number_input("Enter Latitude", value=0.0, format="%.6f")
        longitude = st.number_input("Enter Longitude", value=0.0, format="%.6f")

        if st.button("Check Location"):
            point = Point(longitude, latitude)
            zone = data[data.contains(point)]

            if not zone.empty:
                features = zone[['SHAPE_AREA', 'SHAPE_LEN']]
                prediction = model.predict(features)

                if prediction[0] == 1:
                    st.success("✅ This is a RESIDENTIAL area.")
                else:
                    st.error("❌ This is NOT a residential area.")

                # Show location on a map
                m = folium.Map(location=[latitude, longitude], zoom_start=15)
                folium.Marker([latitude, longitude], popup="Your Location", icon=folium.Icon(color="blue")).add_to(m)
                folium_static(m)
            else:
                st.warning("⚠️ No zoning data found for this location.")

    else:
        st.write("I can help you check residential zoning. Try asking: 'Is my location residential?'")