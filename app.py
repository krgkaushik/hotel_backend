from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) 

def get_db_connection():
    return mysql.connector.connect(
        host="maglev.proxy.rlwy.net",
        user="root",
        password="syJZQHIqjLCUvdSOGovoWGJGFxYFTepq",
        database="railway",
        port=37342
    )

@app.route('/api/appointments', methods=['POST'])
def book_appointment():
    db = None
    try:
        data = request.json
        db = get_db_connection()
        cursor = db.cursor()
        
        # 1. Register the new patient automatically
        patient_sql = "INSERT INTO Patient (name, age, gender, contact, medical_history) VALUES (%s, %s, %s, %s, %s)"
        patient_values = (data['patient_name'], 0, 'Not Specified', 'Not Provided', 'Web Registration')
        cursor.execute(patient_sql, patient_values)
        
        # 2. Get the new patient_id from the last insert
        new_patient_id = cursor.lastrowid
        
        # 3. Book the appointment using that ID
        app_sql = "INSERT INTO Appointment (patient_id, doctor_id, date, time, status) VALUES (%s, %s, %s, %s, %s)"
        app_values = (new_patient_id, data['doctor_id'], data['date'], data['time'], 'Scheduled')
        
        cursor.execute(app_sql, app_values)
        db.commit()
        
        return jsonify({"message": f"Success! {data['patient_name']} is registered and booked."}), 201
        
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database Error: {err}"}), 500
    finally:
        if db and db.is_connected():
            cursor.close()
            db.close()

if __name__ == '__main__':
    app.run(debug=True)
