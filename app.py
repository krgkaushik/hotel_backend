from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
# This allows your Netlify frontend to talk to this backend
CORS(app) 

def get_db_connection():
    return mysql.connector.connect(
        host="maglev.proxy.rlwy.net",
        user="root",
        password="syJZQHIqjLCUvdSOGovoWGJGFxYFTepq",
        database="railway",
        port=37342
    )

# A simple route to test if the server is alive
@app.route('/', methods=['GET'])
def home():
    return "Hospital Backend is Live and Running!"

@app.route('/api/appointments', methods=['POST'])
def book_appointment():
    try:
        data = request.json
        
        # Connect to the database ONLY when someone makes a request
        db = get_db_connection()
        cursor = db.cursor()
        
        # Insert into MySQL Appointment table
        sql = "INSERT INTO Appointment (patient_id, doctor_id, date, time, status) VALUES (%s, %s, %s, %s, %s)"
        values = (data['patient_id'], data['doctor_id'], data['date'], data['time'], 'Scheduled')
        
        cursor.execute(sql, values)
        db.commit()
        
        cursor.close()
        db.close()
        
        return jsonify({"message": "Appointment successfully booked!"}), 201
        
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database Error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
