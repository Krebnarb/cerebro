import os
import csv
import requests
from PIL import Image
from pillow_heif import register_heif_opener
import piexif
import plotly.express as px
from datetime import datetime
from sklearn.cluster import DBSCAN
import numpy as np
from geopy.distance import geodesic
import plotly.graph_objects as go
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Register HEIF/HEIC support with Pillow
register_heif_opener()

# Replace with your OpenCage Geocoder API key
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

def get_decimal_from_dms(dms, ref):
    """Convert DMS (degrees, minutes, seconds) to decimal degrees."""
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1]
    seconds = dms[2][0] / dms[2][1]

    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def extract_gps_and_time(image_path):
    """Extract GPS coordinates and capture time from an image file."""
    try:
        img = Image.open(image_path)
        exif_data = img.info.get("exif")

        if exif_data:
            exif_dict = piexif.load(exif_data)

            # Extract GPS data
            gps_data = exif_dict.get("GPS")
            gps_latitude = gps_data.get(piexif.GPSIFD.GPSLatitude) if gps_data else None
            gps_latitude_ref = gps_data.get(piexif.GPSIFD.GPSLatitudeRef, b'').decode() if gps_data else None
            gps_longitude = gps_data.get(piexif.GPSIFD.GPSLongitude) if gps_data else None
            gps_longitude_ref = gps_data.get(piexif.GPSIFD.GPSLongitudeRef, b'').decode() if gps_data else None

            if gps_latitude and gps_longitude:
                lat = get_decimal_from_dms(gps_latitude, gps_latitude_ref)
                lon = get_decimal_from_dms(gps_longitude, gps_longitude_ref)
            else:
                lat, lon = None, None

            # Extract capture time
            datetime_data = exif_dict.get("Exif", {}).get(piexif.ExifIFD.DateTimeOriginal, b'').decode()
            capture_time = datetime.strptime(datetime_data, "%Y:%m:%d %H:%M:%S") if datetime_data else None

            return lat, lon, capture_time
    except Exception as e:
        print(f"Error extracting data from {image_path}: {e}")

    return None, None, None

def find_image_files(directory):
    """Find all .jpg and .heic files in the given directory."""
    supported_extensions = (".jpg", ".jpeg", ".heic")
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(supported_extensions)
    ]

def get_nearest_city(lat, lon):
    """Get the nearest city for the given GPS coordinates using OpenCage API."""
    try:
        url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={OPENCAGE_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                city = data["results"][0]["components"].get("city", 'NULL')
                country = data["results"][0]["components"].get("country", "UNK")
                
                if city != 'NULL':
                    return f"{city}, {country}"
                else:
                    return f"{country}"
    except Exception as e:
        print(f"Error fetching city for coordinates ({lat}, {lon}): {e}")
    return "Unknown City"

def cluster_coordinates(locations,location_to_file, max_distance_miles):
    """Cluster GPS coordinates using DBSCAN."""
    # Convert max distance from miles to radians (needed for Haversine metric)
    max_distance_km = max_distance_miles * 1.60934
    max_distance_radians = max_distance_km / 6371.0

    # Extract lat/lon as a numpy array
    coordinates = np.array([(loc[0], loc[1]) for loc in locations])

    # Apply DBSCAN clustering
    clustering = DBSCAN(eps=max_distance_radians, min_samples=1, metric='haversine').fit(np.radians(coordinates))

    # Group locations by cluster
    clusters = {}
    cluster_to_files = {}
    for idx, label in enumerate(clustering.labels_):
        if label not in clusters:
            clusters[label] = []
            cluster_to_files[label] = []
        clusters[label].append(locations[idx])
        cluster_to_files[label].append(location_to_file[locations[idx]])

    return clusters, cluster_to_files

def compute_average_date(cluster_points):
    """Compute the average datetime for a cluster."""
    if not cluster_points:
        return None
    timestamps = [p[2].timestamp() for p in cluster_points if p[2] is not None]
    if timestamps:
        avg_timestamp = sum(timestamps) / len(timestamps)
        return datetime.fromtimestamp(avg_timestamp)
    return None

def plot_clusters_with_connections(clusters, directory, cluster_to_filenames):
    """Plot GPS clusters on a map with cluster labels and save the map and metadata."""
    cluster_centers = []
    cluster_labels = []
    cluster_dates = []

    meta_data = []

    for cluster_id, cluster_points in clusters.items():
        # Calculate the cluster center
        lats = [p[0] for p in cluster_points]
        lons = [p[1] for p in cluster_points]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)

        # Compute the average date for the cluster
        avg_date = compute_average_date(cluster_points)
        cluster_dates.append(avg_date)

        # Get a label for the cluster
        city_label = get_nearest_city(center_lat, center_lon)
        cluster_labels.append(city_label)
        cluster_centers.append((center_lat, center_lon))

        # Map filenames to metadata
        for filename in cluster_to_filenames[cluster_id]:
            capture_time = next((p[2] for p in cluster_points if p[2] is not None), None)
            meta_data.append({
                "file_name": os.path.basename(filename),
                "date_taken": capture_time.strftime('%Y-%m-%d %H:%M:%S') if capture_time else "Unknown",
                "city_country_name": city_label,
                "lat": center_lat,
                "lon": center_lon
            })

    # Sort clusters by date
    sorted_clusters = sorted(zip(cluster_centers, cluster_labels, cluster_dates), key=lambda x: x[2] or datetime.min)

    # Extract data for plotting
    latitudes = [c[0][0] for c in sorted_clusters]
    longitudes = [c[0][1] for c in sorted_clusters]
    labels = [c[1] for c in sorted_clusters]

    # Plot clusters
    fig = px.scatter_mapbox(
        lat=latitudes,
        lon=longitudes,
        zoom=5,
        mapbox_style="open-street-map",
        title="Clustered Locations with Chronological Connections",
    )

    fig.update_traces(marker=dict(size=20, color='green', opacity=0.5, symbol='circle'))

    # Add connections between clusters (lines connecting points)
    line_trace = px.line_mapbox(lat=latitudes, lon=longitudes).data[0]
    fig.add_trace(line_trace)

    # Add text labels
    fig.add_trace(go.Scattermapbox(
        lat=latitudes,
        lon=longitudes,
        text=labels,
        mode='text',
        textfont=dict(size=14, color='black'),
        showlegend=False
    ))

    # Save metadata as CSV
    meta_csv_path = os.path.join(directory, "meta.csv")
    with open(meta_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["file_name", "date_taken", "city_country_name", "lat", "lon"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(meta_data)

    fig.show()

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Invalid directory: {directory}")
        sys.exit(1)

    # Find all images and extract their GPS, time, and city data
    image_files = find_image_files(directory)
    locations = []
    location_to_file = {}

    for image_file in image_files:
        lat, lon, capture_time = extract_gps_and_time(image_file)
        if lat is not None and lon is not None:
            location = (lat, lon, capture_time)
            locations.append(location)
            location_to_file[location] = image_file

    # Cluster locations based on 100-mile radius
    clusters, cluster_to_files = cluster_coordinates(locations, location_to_file, max_distance_miles=100)

    # Plot clusters and save outputs
    plot_clusters_with_connections(clusters, directory, cluster_to_files)
