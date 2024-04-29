import pandas as pd
from sklearn.neighbors import NearestNeighbors
import requests

# Function to get the distance between two coordinates using Mapbox API
def get_distance(coords1, coords2):
    access_token = "pk.eyJ1Ijoic2FuaWthZCIsImEiOiJjbHVrNGdmcjgwZnB0MmpsNXUwdmcyMDR6In0.M4cFaJUCdMnCT0plVTnqVQ"
    url = f"https://api.mapbox.com/directions-matrix/v1/mapbox/driving/{coords1[1]},{coords1[0]};{coords2[1]},{coords2[0]}"
    params = {
        'access_token': access_token
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        data = response.json()
        distance_meters = data['durations'][0][1]  
        distance_km = distance_meters / 1000  
        return distance_km
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API request: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Invalid data format in the API response: {e}")
        return None

# Load datasets
buildings_data = pd.read_csv("25_buildings.csv")
neighborhood_data = pd.read_csv("neighborhood.csv")

priority_mapping = {
    1: "School",
    2: "Hospital",
    3: "Railway Station",
    4: "Metro Station"
}

# Function to get ML results based on selected neighborhood priorities
def get_ml_results(priority_input1, priority_input2):
    # Validate inputs
    if priority_input1 not in priority_mapping or priority_input2 not in priority_mapping or priority_input1 == priority_input2:
        print("Invalid inputs. Please enter two different numbers between 1 and 4.")
        return None
    
    selected_priority1 = priority_mapping[priority_input1]
    selected_priority2 = priority_mapping[priority_input2]
    print("Your selected priorities are:", selected_priority1, "and", selected_priority2)

    # Filter neighborhood data based on selected priorities
    filtered_neighborhood_data1 = neighborhood_data[neighborhood_data['n_type'] == selected_priority1].reset_index(drop=True)
    filtered_neighborhood_data2 = neighborhood_data[neighborhood_data['n_type'] == selected_priority2].reset_index(drop=True)

    # Preprocess buildings dataset
    X_buildings = buildings_data[['Latitude', 'Longitude']]

    # Preprocess neighborhood data for both priorities
    X_neighborhood1 = filtered_neighborhood_data1[['Latitude', 'Longitude']]
    X_neighborhood2 = filtered_neighborhood_data2[['Latitude', 'Longitude']]

    # KNN to find nearest neighbors for both priorities
    knn1 = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(X_neighborhood1)
    _, indices1 = knn1.kneighbors(X_buildings)

    knn2 = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(X_neighborhood2)
    _, indices2 = knn2.kneighbors(X_buildings)

    # Calculate distances using Mapbox API for both priorities and find combined distance
    distances_km = []
    nei = []  # List to store the result
    for i in range(len(buildings_data)):
        coords1 = (buildings_data.loc[i, 'Latitude'], buildings_data.loc[i, 'Longitude'])
        coords2_1 = (filtered_neighborhood_data1.loc[indices1[i][0], 'Latitude'], filtered_neighborhood_data1.loc[indices1[i][0], 'Longitude'])
        coords2_2 = (filtered_neighborhood_data2.loc[indices2[i][0], 'Latitude'], filtered_neighborhood_data2.loc[indices2[i][0], 'Longitude'])

        distance_km1 = get_distance(coords1, coords2_1)
        distance_km2 = get_distance(coords1, coords2_2)

        combined_distance = distance_km1 + distance_km2
        distances_km.append(combined_distance)

        # Append to nei list
        nei.append({
            "Building_ID": buildings_data.loc[i, 'prop_id'],
            "Building_Name": buildings_data.loc[i, 'prop_name'],
            "Distance_to_Nearest_Neighborhood_Combined": combined_distance
        })

    # Add nearest neighborhood information and distance to buildings dataset
    buildings_data['Nearest_Neighborhood_ID1'] = filtered_neighborhood_data1.iloc[indices1.flatten()]['n_id'].values
    buildings_data['Nearest_Neighborhood_ID2'] = filtered_neighborhood_data2.iloc[indices2.flatten()]['n_id'].values
    buildings_data['Distance_to_Nearest_Neighborhood_Combined'] = distances_km

    # Sort buildings by combined distance
    sorted_buildings_data = buildings_data.sort_values(by='Distance_to_Nearest_Neighborhood_Combined')

    # Print top 5 recommended buildings
    recommended_buildings = []
    if len(sorted_buildings_data) > 0:
        for index, row in sorted_buildings_data.head(5).iterrows():
            nearest_neighborhood_name1 = filtered_neighborhood_data1[
                filtered_neighborhood_data1['n_id'] == row['Nearest_Neighborhood_ID1']]['n_name'].iloc[0]
            nearest_neighborhood_name2 = filtered_neighborhood_data2[
                filtered_neighborhood_data2['n_id'] == row['Nearest_Neighborhood_ID2']]['n_name'].iloc[0]
            
            building_info = {
                "Building_ID": row['prop_id'],
                "Building_Name": row['prop_name'],
                "Nearby_" + selected_priority1: {
                    "Neighborhood_ID": row['Nearest_Neighborhood_ID1'],
                    "Neighborhood_Name": nearest_neighborhood_name1
                },
                "Nearby_" + selected_priority2: {
                    "Neighborhood_ID": row['Nearest_Neighborhood_ID2'],
                    "Neighborhood_Name": nearest_neighborhood_name2
                },
                "Combined_Distance_km": row['Distance_to_Nearest_Neighborhood_Combined']
            }
            
            recommended_buildings.append(building_info)
    else:
        recommended_buildings = "No results"

    return recommended_buildings, nei  # Return both recommended_buildings and nei

if __name__ == "__main__":
    # Select the preferred neighborhood priorities
    print("Select your two preferred neighborhood priorities:")
    print("1. School")
    print("2. Hospital")
    print("3. Railway Station")
    print("4. Metro Station")
    
    priority_input1 = int(input("Enter the number corresponding to your first preferred priority: "))
    priority_input2 = int(input("Enter the number corresponding to your second preferred priority: "))
    result, nei = get_ml_results(priority_input1, priority_input2)
    print("Recommended buildings:", result)
    print("nei list:", nei)
