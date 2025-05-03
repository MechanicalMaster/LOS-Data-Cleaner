import json
import re
from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile

app = Flask(__name__)

def process_data(file_content):
    # Parse the JSON-like data from the text file
    # The file doesn't have proper JSON format, so we need to extract the data
    
    # Regex to extract the data array
    match = re.search(r'"updatedByUserListDetails":\s*(\[.*?\])', file_content, re.DOTALL)
    if not match:
        return {"error": "Could not parse input file"}
    
    data_str = match.group(1)
    
    # Add proper JSON formatting
    try:
        data = json.loads(data_str)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in input file"}
    
    # Sort data by time to ensure chronological order
    data.sort(key=lambda x: x.get('time', 0))
    
    # Initialize the result structure
    result = []
    current_status = None
    current_status_data = None
    
    for entry in data:
        status = entry.get('applicationstatus')
        timestamp = entry.get('time')
        user_id = entry.get('user_id')
        phase = entry.get('phase')
        task_name = entry.get('taskName')
        
        # Skip entries with missing required fields
        if not all([status, timestamp, user_id]):
            continue
        
        # If this is a new status or the first entry
        if current_status != status:
            # Close previous status entry if it exists
            if current_status_data:
                current_status_data['status_end_time'] = timestamp
                result.append(current_status_data)
            
            # Create new status entry
            current_status = status
            current_status_data = {
                'status': status,
                'status_start_time': timestamp,
                'status_end_time': None,  # Will be populated when status changes
                'user_id': user_id,
                'phase': phase,
                'task_name': task_name
            }
    
    # Add the last status (which doesn't have an end time)
    if current_status_data:
        result.append(current_status_data)
    
    return {"status_history": result}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file_content = file.read().decode('utf-8')
    result = process_data(file_content)
    
    if 'error' in result:
        return jsonify(result), 400
    
    # Create a temporary file to send as download
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    temp_file_name = temp_file.name
    with open(temp_file_name, 'w') as f:
        json.dump(result, f, indent=2)
    
    return send_file(
        temp_file_name,
        mimetype='application/json',
        as_attachment=True,
        download_name='processed_data.json'
    )

if __name__ == '__main__':
    app.run(debug=True) 