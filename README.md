# LOS Data Cleaner

A simple Python web application that processes Loan Origination System (LOS) log data and outputs a clean JSON file showing the status history of each case.

## Features

- Processes raw LOS log data from text files
- Extracts status changes and their timestamps
- Identifies the user who initiated each status change
- Provides a clean, structured JSON output with sequential numbering
- Converts Unix timestamps to human-readable date and time format
- Simple web interface for uploading files

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd los_cleaner
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the dependencies:
```
pip install -r requirements.txt
```

## Usage

1. Start the application:
```
python app.py
```

2. Open your web browser and navigate to http://127.0.0.1:5000

3. Upload a LOS data file (like the example Dealer_887.txt)

4. The application will process the file and provide a JSON download with the cleaned data

## Input Format

The application expects a text file containing JSON-like data with an "updatedByUserListDetails" array. Example:

```
"updatedByUserListDetails": [
    {
        "phase": "Leads/Applications",
        "role": "Business User",
        "user_id": 20,
        "taskName": null,
        "time": 1734934378481,
        "applicationstatus": "Lead Uploaded"
    },
    ...
]
```

## Output Format

The application generates a structured JSON file with the following format:

```json
{
  "status_history": [
    {
      "sr_no": 1,
      "status": "Lead Uploaded",
      "status_start_time": 1734934378481,
      "status_start_time_readable": "2024-12-23 10:32:58",
      "status_end_time": 1735999948223,
      "status_end_time_readable": "2025-01-05 08:12:28",
      "user_id": 20,
      "phase": "Leads/Applications",
      "task_name": null
    },
    {
      "sr_no": 2,
      "status": "Customer Consent Provided",
      "status_start_time": 1735999948223,
      "status_start_time_readable": "2025-01-05 08:12:28",
      "status_end_time": 1736000829556,
      "status_end_time_readable": "2025-01-05 08:27:09",
      "user_id": 20,
      "phase": "Leads/Applications",
      "task_name": "Consent Form"
    },
    ...
  ]
}
```

## Rules Applied

The data processing follows these rules:

1. Only the first occurrence of each status is recorded (ignores multiple saves in the same status)
2. The status end time is set to the timestamp of the first occurrence of the next status
3. The last status has a null end time
4. The user ID is recorded from the first occurrence of each status
5. Each status entry is sequentially numbered with a Sr. No field
6. All Unix timestamps are also provided in human-readable format (YYYY-MM-DD HH:MM:SS) 