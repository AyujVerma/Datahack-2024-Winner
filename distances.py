from math import radians, sin, cos, sqrt, atan2

# Function to calculate distance between two geographical coordinates using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    # Calculate the change in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    # Apply Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance

# Dictionary to store the coordinates of each city
city_coordinates = {
    'Royals': (39.0513, -94.4805),     # Kansas City (Royals)
    'Braves': (33.8908, -84.4679),     # Atlanta (Braves)
    'Rays': (27.7684, -82.6483),       # St. Petersburg (Rays)
    'Blue Jays': (43.6414, -79.3894),  # Toronto (Blue Jays)
    'Diamondbacks': (33.4455, -112.0667),  # Phoenix (Diamondbacks)
    'Astros': (29.7572, -95.3554),     # Houston (Astros)
    'Pirates': (40.4469, -80.0057),    # Pittsburgh (Pirates)
    'Dodgers': (34.0736, -118.2400),   # Los Angeles (Dodgers)
    'Rockies': (39.7554, -104.9881),   # Denver (Rockies)
    'Nationals': (38.8729, -77.0074),  # Washington D.C. (Nationals)
    'Cardinals': (38.6226, -90.1928),  # St. Louis (Cardinals)
    'Red Sox': (42.3467, -71.0972),    # Boston (Red Sox)
    'Orioles': (39.2839, -76.6217),    # Baltimore (Orioles)
    'Giants': (37.7786, -122.3893),    # San Francisco (Giants)
    'Reds': (39.0979, -84.5086),       # Cincinnati (Reds)
    'Indians': (41.4959, -81.6853),    # Cleveland (Indians)
    'Padres': (32.7076, -117.1570),    # San Diego (Padres)
    'Phillies': (39.9054, -75.1669),   # Philadelphia (Phillies)
    'White Sox': (41.8301, -87.6347),  # Chicago (White Sox)
    'Brewers': (43.0280, -87.9712),    # Milwaukee (Brewers)
    'Yankees': (40.8296, -73.9262),    # New York City (Yankees)
    'Mets': (40.7571, -73.8458),       # New York City (Mets)
    'Rangers': (32.7511, -97.0820),    # Arlington (Rangers)
    'Marlins': (25.7780, -80.2195),    # Miami (Marlins)
    'Mariners': (47.5914, -122.3325),  # Seattle (Mariners)
    'Twins': (44.9817, -93.2784),      # Minneapolis (Twins)
    'Angels': (33.8003, -117.8827),    # Anaheim (Angels)
    'Cubs': (41.9484, -87.6553),       # Chicago (Cubs)
    'Athletics': (37.7516, -122.2005), # Oakland (Athletics)
    'Tigers': (42.3391, -83.0487)      # Detroit (Tigers)
}

# Dictionary to store the total distance traveled by each away team
total_distance = {}

# Dictionary to store the number of games played by each away team
games_played = {}

# Parse the data and calculate distances
with open('example_data/schedules/2014_schedule.csv', 'r') as file:
    next(file)  # Skip header
    for line in file:
        year, day, home_team, away_team = line.strip().split(',')[0:4]
        
        # Check if coordinates for both cities are available
        if home_team in city_coordinates and away_team in city_coordinates:
            home_lat, home_lon = city_coordinates[home_team]
            away_lat, away_lon = city_coordinates[away_team]
            
            # Calculate distance between home and away cities
            distance = calculate_distance(home_lat, home_lon, away_lat, away_lon)
            
            # Update total distance and games played for the away team
            total_distance[away_team] = total_distance.get(away_team, 0) + distance
            games_played[away_team] = games_played.get(away_team, 0) + 1

# Calculate average distance traveled per game for each away team
average_distance_per_game = {team: total_distance[team] / games_played[team] for team in total_distance}

# Display the average distance traveled for each away team
for team, distance in average_distance_per_game.items():
    print(f"{team}: {distance:.2f} km")
