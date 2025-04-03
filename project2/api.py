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
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        data = request.get_json()

        
        course_id = data.get('course_id')
        semester = data.get('semester')
        year = data.get('year')
        instructor = data.get('instructor')


        #Checking if the section has a course that exists
        cursor.execute("SELECT 1 FROM courses WHERE course_id = ?", (course_id,))
        exists = cursor.fetchone() is not None

        if exists:
            cursor.execute("""
            INSERT INTO sections (course_id, semester, year, instructor) VALUES ( ?, ?, ?, ?)""",
            (course_id, semester, year, instructor))
            conn.commit()
            conn.close()

            return jsonify({'message': 'Section Added Successfully'}), 200
        else:
            conn.commit()
            conn.close()
            return jsonify({'message': 'The course for this section does not exist'}), 400

    except Exception as e:
         print(f"Error: {str(e)}")
         return jsonify({'error': str(e)}), 500
    


# Search Sections by Course ID
@app.route('/api/search_sections', methods=['GET'])
def search_sections():
    try:
        course_id = request.args.get('course_id')

        if not course_id:
            return jsonify({'error': 'course_id parameter is required'}), 400

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sections WHERE course_id = ?", (course_id,))
        sections = cursor.fetchall()
        conn.close()

        if not sections:
            return jsonify({'message': 'No sections found for the given course_id'}), 404

        # Convert results into a list of dictionaries
        section_list = []
        for section in sections:
            section_dict = {
                'section_id': section[0],
                'course_id': section[1],
                'semester': section[2],
                'year': section[3],
                'instructor': section[4],
            }
            section_list.append(section_dict)

        return jsonify({'sections': section_list})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Function to execute raw SQL queries
def execute_query(query, params=None):
    conn = sqlite3.connect(DATABASE)
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchall()  # Fetch all results
    return result

# predefined query helper functions
def search_student_by_id(value):
    query = "SELECT * FROM students WHERE id = %s"
    return execute_query(query, [value])

def search_student_by_city(value):
    query = "SELECT * FROM students WHERE city = %s"
    return execute_query(query, [value])

def search_student_by_zip(value):
    query = "SELECT * FROM students WHERE zipcode = %s"
    return execute_query(query, [value])

def search_student_by_email(value):
    query = "SELECT * FROM students WHERE email = %s"
    return execute_query(query, [value])

def search_student_by_first(value):
    query = "SELECT * FROM students WHERE first_name LIKE %s"
    return execute_query(query, ['%' + value + '%'])

def search_student_by_last(value):
    query = "SELECT * FROM students WHERE last_name LIKE %s"
    return execute_query(query, ['%' + value + '%'])

def search_student_by_full(first_name, last_name):
    query = "SELECT * FROM students WHERE first_name LIKE %s AND last_name LIKE %s"
    return execute_query(query, ['%' + first_name + '%', '%' + last_name + '%'])

def search_course_by_id(value):
    query = "SELECT * FROM courses WHERE course_id = %s"
    return execute_query(query, [value])

def search_course_by_rubric(value):
    query = "SELECT * FROM courses WHERE course_id = %s"
    return execute_query(query, [value])

def search_course_by_credit(value):
    query = "SELECT * FROM courses WHERE credits = %s"
    return execute_query(query, [value])

def search_course_by_sem_year_rub(semester, year, rubric):
    query = "SELECT * FROM courses WHERE semester = %s AND year = %s AND rubric = %s"
    return execute_query(query, [semester, year, rubric])

def search_section_by_id(value):
    query = "SELECT * FROM sections WHERE section_id = %s"
    return execute_query(query, [value])

def search_section_by_semester(value):
    query = "SELECT * FROM sections WHERE semester = %s"
    return execute_query(query, [value])

def search_section_by_year(value):
    query = "SELECT * FROM sections WHERE year = %s"
    return execute_query(query, [value])

def search_section_by_course(value):
    query = "SELECT * FROM sections WHERE course_id = %s"
    return execute_query(query, [value])

def search_section_by_instructor(value):
    query = "SELECT * FROM sections WHERE instructor LIKE %s"
    return execute_query(query, ['%' + value + '%'])


# dictionary - maps query options to handler functions
QUERY_HANDLERS = {
    'student_by_id': search_student_by_id,
    'student_by_city': search_student_by_city,
    'student_by_zip': search_student_by_zip,
    'student_by_email': search_student_by_email,
    'student_by_first': search_student_by_first,
    'student_by_last': search_student_by_last,
    'student_by_full': search_student_by_full,
    'course_by_id': search_course_by_id,
    'course_by_rubric': search_course_by_rubric,
    'course_by_credit': search_course_by_credit,
    'course_by_sem_year_rub': search_course_by_sem_year_rub,
    'section_by_id': search_section_by_id,
    'section_by_semester': search_section_by_semester,
    'section_by_year': search_section_by_year,
    'section_by_course': search_section_by_course,
    'section_by_instructor': search_section_by_instructor,
}
#route for queries
@app.route('/api/search', methods=['POST'])
def query():
    try:
        query_type = request.POST.get('option')
        data = {}

        if handler:
            if query_type == 'student_by_full':
                first_name = request.POST.get('First Name')
                last_name = request.POST.get('Last Name')

    except Exception as e:
        return jsonify({'error': str(e)}), 500    

    

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")