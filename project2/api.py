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

# Get all courses
@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        conn.close()

        course_list = []
        for course in courses:
            course_dict = {
                'course_id': course[0],
                'course_name': course[1],
                'course_description': course[2],
                'number_credits': course[3],
            }

            course_list.append(course_dict)
        
        return jsonify({'courses': course_list})
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
@app.route('/api/add_course', methods=['POST'])
def add_course():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        data = request.get_json()

        course_id = data.get('course_id')
        course_name = data.get('course_name')
        course_description = data.get('course_description')
        number_credits = data.get('number_credits')

        cursor.execute("""
        INSERT INTO courses (course_id, course_name, course_description, number_credits) VALUES (?, ?, ?, ?)
                        """,(course_id, course_name, course_description, number_credits))
        
        conn.commit()
        conn.close()

        return jsonify({'message': 'Course Added Successfully'}), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
# Add section
@app.route('/api/add_section', methods = ['POST'])
def add_section():
    #Section id
    #course id
    #semster
    #year
    #instructor
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        data = request.get_json()

        #section_id = data.get('section_id')
        course_id = data.get('course_id')
        semester = data.get('semester')
        year = data.get('year')
        instructor = data.get('instructor')

        cursor.execute("""
        INSERT INTO sections ( course_id, semester, year, instructor) VALUES ( ?, ?, ?, ?)""",
        ( course_id, semester, year, instructor))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Section Added Successfully'}), 200
    except Exception as e:
         print(f"Error: {str(e)}")
         return jsonify({'error': str(e)}), 500
    

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")