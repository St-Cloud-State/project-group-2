from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Define the path to your SQLite database file
DATABASE = 'university.db'

# get all students
@app.route('/api/students', methods=['GET'])
def get_all_students():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        conn.close()

        # Convert the list of tuples into a list of dictionaries
        student_list = []
        for student in students:
            student_dict = {
                'student_id': student[0],
                'first_name': student[1],
                'last_name': student[2],
                'date_of_birth': student[3],
                'email': student[4],
                'address': student[5],
                'phone': student[6],
                # Add other attributes here as needed
            }
            student_list.append(student_dict)

        return jsonify({'students': student_list})
    except Exception as e:
        return jsonify({'error': str(e)})

# Add Student
@app.route('/api/add_student', methods=['POST'])
def add_student():
    try:    
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        dob = data.get('dob')
        email = data.get('email')
        address = data.get('address')
        phone = data.get('phone')

        cursor.execute("""
        INSERT INTO students (first_name, last_name, date_of_birth, email, address, phone) VALUES (?, ?, ?, ?, ?, ?)
                       """,(first_name, last_name, dob, email, address, phone))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Student Added Successfully'}), 200

    except Exception as e:
        print(f"Error: {str(e)}") 
        return jsonify({'error': str(e)}), 500

# Add Course

# Add section

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")