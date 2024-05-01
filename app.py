from flask import Flask, render_template, jsonify, request
import json
from ml.priority import getMLResults
# from models import db  # Import db (SQLAlchemy instance) from models
import os

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('instance/config.py', silent=True)
# Update the database URI
nei = []

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
# # Initialize the SQLAlchemy instance with the Flask app
# db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    with open('./data.json') as f:
        buildings = json.load(f)

    # Assuming each building object in the JSON file has a unique 'id' attribute
    for building in buildings:
        building['id'] = building['prop_id'] 
    # Filter by location
    location_filter = request.args.get('location')
    if location_filter:
        buildings = [building for building in buildings if location_filter.lower() in building['prop_addr'].lower()]
    
    # Filter by BHK
    bhk_filter = request.args.get('bhk')
    if bhk_filter:
        buildings = [building for building in buildings if building['bhk'] == int(bhk_filter)]
    
    # Filter by price range
    price_range_filter = request.args.get('price_range')
    if price_range_filter:
        min_price, max_price = map(int, price_range_filter.split('-'))
        buildings = [building for building in buildings if min_price <= building['price'] <= max_price]
    
    return render_template('index.html', buildings=buildings)

@app.route('/property_details/<int:prop_id>')
def pproperty_details(prop_id):
    with open('./data.json') as f:
        properties = json.load(f)
    
    # Assuming 'prop_id' is a unique identifier for each property
    property = next((prop for prop in properties if prop['prop_id'] == prop_id), None)
    
    if property:
        return render_template('filter.html', property=property)
    else:
        # Handle the case where the property with the given ID is not found
        return "Property not found", 404


@app.route('/property/', methods=['GET', 'POST'])
def property_view():
    global nei
    f = open('./data.json')
    buildings = json.load(f)
    if request.method == "POST":
        print(request.data)
        print(request.form.get('criteria1'))
        print(request.form.get('criteria2'))
        input1 = request.form.get('criteria1')
        if not input1:
            input1 = 1
        input2 = request.form.get('criteria2')
        if not input2:
            input2 = 1
        mlres = getMLResults(int(input1), int(input2))
        newbldg = []
        for i in mlres:
            for j in buildings:
                if i["Building_ID"] == j["prop_id"]:
                    newbldg.append(j)
        print(newbldg)
        buildings = newbldg
        nei = mlres
    print(nei) 
    return render_template('property.html', buildings=buildings)

# @app.route('/property/<int:prop_id>/')
# def property_details(prop_id):
#     global nei
#     print("MMLLLLLL")
#     print(nei)
    
#     # Search for the prop_id in nei list
#     for build in nei:
#         if build["Building_ID"] == prop_id:
#             print("millllll")
#             print(jsonify(build))  # Return the data if found
    
#     # Return a message if the prop_id is not found
#     # return jsonify({"message": "Building not found"})


#     # # Find the property with the given prop_id
#     # property = next((b for b in nei if b['Building_ID'] == prop_id), None)

#     # if property:
#     #     # Assuming 'nearby' information is already stored in the 'nei' list
#     #     property["nearby_school"] = property.get("Nearby_School", "")
#     #     property["nearby_hospital"] = property.get("Nearby_Hospital", "")
#     #     property["nearby_railway"] = property.get("Nearby_Railway Station", "")
#     #     property["nearby_metro"] = property.get("Nearby_Metro Station", "")
#     # else:
#     #    print("Property not found for prop_id:", prop_id)

#     return render_template('prop1.html', property=property)
from flask import render_template, jsonify
import json

@app.route('/property/<int:prop_id>/')
def property_details(prop_id):
    global nei
    f = open('./data.json')
    buildings = json.load(f)
    property = {}
    for i in buildings:
        if i["prop_id"] == prop_id:
            property = i
            break
    else:
        return jsonify({"message": "Property not found for prop_id: {}".format(prop_id)}), 404

    # Find the property with the given prop_id
    prop_id = int(prop_id)  # Convert prop_id to integer
    for build in nei:
        if build["Building_ID"] == prop_id:
            print("milllaaa")
            print(build)
            strnei_bytes = jsonify(build).data  # Convert the JSON object to a bytes-like object
            strnei_str = strnei_bytes.decode('utf-8')  # Decode the bytes-like object to a string
            strnei_cleaned = strnei_str.replace('\\n', '').replace('\n', '').replace('\\r', '').replace('\r', '').replace('"', '').replace('{', '').replace('}', '')  # Remove unwanted characters
            strnei_lines = strnei_cleaned.split(', ')  # Split the string into lines by comma followed by space
            formatted_lines = []  # List to store formatted lines
            for line in strnei_lines:
                if "Nearby" in line:  # If the line contains the word "Nearby", start on a new line
                    formatted_lines.append('\n' + line)
                else:
                    formatted_lines.append(line)
            strnei_formatted = ', '.join(formatted_lines)  # Join the lines back together with commas
            return render_template('prop1.html', strnei=strnei_formatted, property=property)  # Pass the cleaned string to the template
    else:
        return jsonify({"message": "Property not found for prop_id: {}".format(prop_id)}), 404

    # global nei
    # f = open('./data.json')
    # buildings = json.load(f)
    # # if request.method == "POST":
    # #     print(request.data)
    # #     print(request.form.get('criteria1'))
    # #     print(request.form.get('criteria2'))
    # #     input1 = request.form.get('criteria1')
    # #     if not input1:
    # #         input1 = 1
    # #     input2 = request.form.get('criteria2')
    # #     if not input2:
    # #         input2 = 1
    # #     mlres = getMLResults(int(input1), int(input2))
    # newbldg = []
    # #     for i in mlres:
    # for j in nei:
    #     if j["Building_ID"] == j["prop_id"]:
    #         newbldg.append(j)
    # #     print(newbldg)
    # #     buildings = newbldg
    # #     nei = newbldg

    # property = {}
    # for i in buildings:
    #     if i["prop_id"] == prop_id:
    #         property = i
    #         break

    # # Print the content or status of the 'nei' list
    # if nei:
    #     print("NEI LIST CONTENT:")
    #     for item in nei:
    #         print(item)  # Print each item in the nei list

    #     # Check and update the property if matching Building_ID is found in the 'nei' list
    #     matched_nei = [item for item in nei if item.get("Building_ID") == prop_id]
    #     if matched_nei:
    #         matched_item = matched_nei[0]  # Considering only the first matching item
    #         property["nearby school"] = matched_item.get("Nearby_School", "")
    #         property["nearby hospital"] = matched_item.get("Nearby_Hospital", "")
    #         property["nearby railway"] = matched_item.get("Nearby_Railway Station", "")
    #         property["nearby metro"] = matched_item.get("Nearby_Metro Station", "")
    #     else:
    #         print("No matching item in the NEI list for prop_id:", prop_id)
    # else:
    #     print("NEI LIST IS EMPTY")

    # return render_template('prop1.html', property=property)

@app.route('/fin/')
def fw():
    return render_template('fw.html')

if __name__ == '__main__':
    app.run(debug=True)
