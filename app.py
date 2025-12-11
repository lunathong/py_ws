import csv
import json
import os
import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
CSV_FILE = 'data.csv'

def read_data():
    items = []
    if not os.path.exists(CSV_FILE):
        return items
    
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(row)
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return items

def write_data(items):
    if not items:
        return
    
    fieldnames = ['name', 'value', 'status', 'last_updated']
    try:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(items)
    except Exception as e:
        print(f"Error writing CSV: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/monitor', methods=['GET'])
def get_monitor_data():
    data = read_data()
    return jsonify(data)

@app.route('/api/monitor', methods=['POST'])
def update_monitor_data():
    try:
        payload = request.json
        # Format: "monitoring_item_1", value="1", status="yellow" (as roughly requested)
        # But user example was: "monitoring_item_1", value="1", status="yellow"
        # I'll assume standard JSON keys: name (or item identifier), value, status.
        # Let's support 'name' as the unique key to find and update.
        
        if not payload:
            return jsonify({"error": "No data provided"}), 400

        target_name = payload.get('name') or payload.get('monitoring_item') # generic fallback
        
        # User prompt said: The json payload will format as "monitoring_item_1", value="1", status="yellow"
        # It's a bit ambiguous if monitoring_item_1 is the KEY or the value of a key. 
        # I will assume the payload might look like: {"name": "monitoring_item_1", "value": "1", "status": "yellow"}
        # Or keys are dynamic. Let's stick to strict schema for simplicity but handle standard keys.
        
        if not target_name and 'monitoring_item' not in payload:
             # Try to find the first key that isn't value/status? No, let's look for 'name'.
             # If user sends `{"monitoring_item_1": "somevalue", ...}` that's harder.
             # Let's assume standard: {"name": "CPU Usage", "value": "90%", "status": "red"}
             pass
             
        target_name = payload.get('name')
        new_value = payload.get('value')
        new_status = payload.get('status')
        
        if not target_name:
             return jsonify({"error": "Missing 'name' in payload"}), 400

        items = read_data()
        updated = False
        
        current_time = datetime.datetime.now().isoformat()

        for item in items:
            if item['name'] == target_name:
                if new_value: item['value'] = new_value
                if new_status: item['status'] = new_status
                item['last_updated'] = current_time
                updated = True
                break
        
        if not updated:
            # Add new item
            items.append({
                'name': target_name,
                'value': new_value if new_value else 'N/A',
                'status': new_status if new_status else 'green',
                'last_updated': current_time
            })
        
        write_data(items)
        return jsonify({"message": "Data updated successfully", "data": items})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
