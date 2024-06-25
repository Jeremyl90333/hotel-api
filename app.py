from flask import Flask, request, jsonify

app = Flask(__name__)

# Example data structure based on the sheets summary
hotel_data = {
    "Sheraton": {
        "information": [
            {"name": "Guest Rooms & Suites", "description": "390", "additional_info": ""},
            {"name": "Amenities", "description": "Private balcony or patio, full-size work desk", "additional_info": ""}
        ],
        "meeting_spaces": [
            {"name": "Britannia Ballroom", "description": "9920 sqft", "additional_info": ""}
        ]
    },
    "Marriott": {
        "information": [
            {"name": "Floors", "description": "18", "additional_info": ""},
            {"name": "Guest Rooms & Suites", "description": "65 rooms, 171 suites", "additional_info": ""}
        ],
        "meeting_spaces": [
            {"name": "Marquis Ballroom", "description": "8500 sqft", "additional_info": ""}
        ]
    },
    "Hilton": {
        "information": [
            {"name": "Guest Rooms & Suites", "description": "237 newly renovated guest rooms and suites", "additional_info": ""},
            {"name": "Beds", "description": "Hilton Bed with extra coil support", "additional_info": ""}
        ],
        "meeting_spaces": [
            {"name": "Grand Ballroom", "description": "10000 sqft", "additional_info": ""}
        ]
    }
}

@app.route('/hotel/information', methods=['GET'])
def get_hotel_information():
    hotel = request.args.get('hotel')
    category = request.args.get('category')
    
    if hotel not in hotel_data:
        return jsonify({"error": "Hotel not found"}), 404
    
    details = hotel_data[hotel].get(category.lower(), [])
    return jsonify({
        "hotel": hotel,
        "category": category,
        "details": details
    })

if __name__ == '__main__':
    app.run(debug=True)