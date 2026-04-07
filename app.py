from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="your_database_host",
    user="your_username",
    password="your_password",
    database="hospital_db"
)

@app.route('/api/appointments', methods=['POST'])
def book_appointment():
    data = request.json
    cursor = db.cursor()
    
    # Insert into MySQL Appointment table
    sql = "INSERT INTO Appointment (patient_id, doctor_id, date, time) VALUES (%s, %s, %s, %s)"
    values = (data['patient_id'], data['doctor_id'], data['date'], data['time'])
    
    cursor.execute(sql, values)
    db.commit()
    
    return jsonify({"message": "Appointment successfully booked!"}), 201

if __name__ == '__main__':
    app.run(debug=True)