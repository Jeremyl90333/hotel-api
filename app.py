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
        ],
        "room_rental": [
            {"name": "Deluxe Room", "cost": 250, "additional_info": ""}
        ],
        "catering_menu": [
            {"name": "Breakfast Buffet", "description": "Continental breakfast buffet", "price": 20}
        ]
    },
    "Marriott": {
        "information": [
            {"name": "Floors", "description": "18", "additional_info": ""},
            {"name": "Guest Rooms & Suites", "description": "65 rooms, 171 suites", "additional_info": ""}
        ],
        "meeting_spaces": [
            {"name": "Marquis Ballroom", "description": "8500 sqft", "additional_info": ""}
        ],
        "room_rental": [
            {"name": "Executive Suite", "cost": 350, "additional_info": ""}
        ],
        "catering_menu": [
            {"name": "Lunch Buffet", "description": "International lunch buffet", "price": 35}
        ]
    },
    "Hilton": {
        "information": [
            {"name": "Guest Rooms & Suites", "description": "237 newly renovated guest rooms and suites", "additional_info": ""},
            {"name": "Beds", "description": "Hilton Bed with extra coil support", "additional_info": ""}
        ],
        "meeting_spaces": [
            {"name": "Grand Ballroom", "description": "10000 sqft", "additional_info": ""}
        ],
        "room_rental": [
            {"name": "Presidential Suite", "cost": 500, "additional_info": ""}
        ],
        "catering_menu": [
            {"name": "Dinner Buffet", "description": "Gourmet dinner buffet", "price": 50}
        ]
    }
}

email_templates = {
    "Conference Services Manager Introduction": "I am pleased to introduce (CSM Name), your Conference Services Manager...",
    "Business Evaluation Email to Karla": "Hi Karla, I have a new lead from (Group Name)..."
}

audio_visual_services = [
    {"name": "Projector", "description": "HD Projector", "price": 100},
    {"name": "Microphone", "description": "Wireless microphone", "price": 50}
]

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

@app.route('/room-rental/costs', methods=['GET'])
def get_room_rental_costs():
    hotel = request.args.get('hotel')
    room = request.args.get('room')
    
    if hotel not in hotel_data:
        return jsonify({"error": "Hotel not found"}), 404
    
    room_data = next((r for r in hotel_data[hotel].get("room_rental", []) if r["name"] == room), None)
    if room_data is None:
        return jsonify({"error": "Room not found"}), 404
    
    return jsonify({
        "hotel": hotel,
        "room": room,
        "cost": room_data["cost"],
        "additional_info": room_data.get("additional_info", "")
    })

@app.route('/catering/options', methods=['GET'])
def get_catering_options():
    hotel = request.args.get('hotel')
    menu = request.args.get('menu')
    
    if hotel not in hotel_data:
        return jsonify({"error": "Hotel not found"}), 404
    
    menu_data = next((m for m in hotel_data[hotel].get("catering_menu", []) if m["name"] == menu), None)
    if menu_data is None:
        return jsonify({"error": "Menu not found"}), 404
    
    return jsonify({
        "hotel": hotel,
        "menu": menu,
        "items": [menu_data]
    })

@app.route('/email/generate', methods=['POST'])
def generate_email():
    data = request.json
    template_type = data.get('template_type')
    variables = data.get('variables')
    
    if template_type not in email_templates:
        return jsonify({"error": "Template not found"}), 404
    
    email_content = email_templates[template_type]
    for key, value in variables.items():
        email_content = email_content.replace(f"({key})", value)
    
    return jsonify({
        "template_type": template_type,
        "email_content": email_content
    })

@app.route('/audio-visual/services', methods=['GET'])
def get_audio_visual_services():
    hotel = request.args.get('hotel')
    
    return jsonify({
        "hotel": hotel,
        "services": audio_visual_services
    })

if __name__ == '__main__':
    app.run(debug=True)
