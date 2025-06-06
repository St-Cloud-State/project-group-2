from flask import Flask, jsonify, render_template, request
from datetime import datetime
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
        cursor.execute("SELECT * FROM courses ORDER BY course_id")
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

        # ←–– ADDED: compute the next student_id as “number of rows + 1”
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        new_id = count + 1

        data = request.get_json()
        first_name = data.get('first_name')
        last_name  = data.get('last_name')
        dob        = data.get('dob')
        email      = data.get('email')
        address    = data.get('address')
        phone      = data.get('phone')

        cursor.execute("SELECT 1 from students WHERE first_name = ?", (first_name,))
        firstNameExists = cursor.fetchone() is not None

        cursor.execute("SELECT 1 from students WHERE last_name = ?", (last_name,))
        lastNameExists = cursor.fetchone() is not None

        cursor.execute("SELECT 1 from students WHERE date_of_birth = ?", (dob,))
        birthdayExists = cursor.fetchone() is not None

        # Checks if a person with the same name and birthday already exists
        if firstNameExists and lastNameExists and birthdayExists:
            conn.commit()
            conn.close()
            return jsonify({'message': 'This student already exists'}), 400
        else:
            cursor.execute("""
                INSERT INTO students
                    (student_id, first_name, last_name, date_of_birth, email, address, phone)
                VALUES
                    (?,          ?,          ?,         ?,             ?,      ?,       ?)
            """, (new_id, first_name, last_name, dob, email, address, phone))
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

        cursor.execute("SELECT 1 FROM courses WHERE course_id = ?", (course_id,))
        exists = cursor.fetchone() is None

        if exists:
            cursor.execute("""
                INSERT INTO courses (course_id, course_name, course_description, number_credits)
                VALUES (?, ?, ?, ?)
            """, (course_id, course_name, course_description, number_credits))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Course Added Successfully'}), 200
        else:
            conn.commit()
            conn.close()
            return jsonify({'message': 'This course already exists'}), 400

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Add section
@app.route('/api/add_section', methods=['POST'])
def add_section():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        data = request.get_json()
        course_id = data.get('course_id')
        semester = data.get('semester')
        year = data.get('year')
        instructor = data.get('instructor')

        cursor.execute("SELECT 1 FROM courses WHERE course_id = ?", (course_id,))
        exists = cursor.fetchone() is not None

        if exists:
            cursor.execute("""
                INSERT INTO sections (course_id, semester, year, instructor)
                VALUES (?, ?, ?, ?)
            """, (course_id, semester, year, instructor))
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

# Register a student to a section
@app.route('/api/registerStudent', methods=['POST'])
def registerStudent():
    try:
        data = request.get_json()
        section_info = data.get('section_ID')
        if section_info == 'No Sections Available For This Course':
            return jsonify({'message': 'There are no Sections available for this course'}), 201
        section_id = section_info.split(" ")[0]

        student_id = data.get('student_ID')
        current_date = datetime.now().strftime("%m-%d-%Y")
        grade = 'Z'

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM students WHERE student_id = ?", (student_id,))
            studentExists = cursor.fetchone() is not None

            cursor.execute(
                "SELECT * FROM registrations WHERE student_id = ? AND section_id = ?",
                (student_id, section_id)
            )
            already_registered = cursor.fetchone()

            if not studentExists:
                return jsonify({'message': 'The student does not exist'}), 400
            if already_registered:
                return jsonify({'message': 'The student is already registered for this section'}), 201

            cursor.execute("""
                INSERT INTO registrations (student_id, section_id, date, grade)
                VALUES (?, ?, ?, ?)
            """, (student_id, section_id, current_date, grade))
            conn.commit()
            return jsonify({'message': 'Student registered successfully'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Add a grade to a student's section
@app.route('/api/addGrade', methods=['POST'])
def addGrade():
    try:
        data = request.get_json()
        section_id = data.get('section_ID')
        student_id = data.get('student_ID')
        grade = data.get('grade')

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM students WHERE student_id = ?", (student_id,))
            studentExists = cursor.fetchone() is not None

            cursor.execute("SELECT 1 FROM sections WHERE section_id = ?", (section_id,))
            sectionExists = cursor.fetchone() is not None

            if not studentExists or not sectionExists:
                return jsonify({'message': 'The student or section does not exist'}), 400

            cursor.execute("""
                UPDATE registrations
                SET grade = ?
                WHERE student_id = ? AND section_id = ?
            """, (grade, student_id, section_id))
            conn.commit()
            return jsonify({'message': 'Grade updated successfully'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Print a transcript
@app.route('/api/printTranscript', methods=['POST'])
def printTranscript():
    try:
        data = request.get_json()
        student_id = data.get('student_ID')

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM students WHERE student_id = ?", (student_id,))
            studentExists = cursor.fetchone() is not None

            if studentExists:
                cursor.execute("""
                    SELECT first_name, last_name, student_id, date_of_birth, email, address, phone
                    FROM students WHERE student_id = ?
                """, (student_id,))
                personalInfo = cursor.fetchone()

                cursor.execute("""
                    SELECT courses.course_name, sections.year, registrations.grade
                    FROM registrations
                    JOIN sections ON registrations.section_id = sections.section_id
                    JOIN courses ON sections.course_id = courses.course_id
                    WHERE registrations.student_id = ?
                """, (student_id,))
                courseData = cursor.fetchall()

                with open(f"transcript_for_{student_id}.txt", "w") as outfile:
                    outfile.write(
                        f"Name: {personalInfo[0]} {personalInfo[1]}\n"
                        f"ID: {personalInfo[2]}\n"
                        f"DOB: {personalInfo[3]}\n"
                        f"Email: {personalInfo[4]}\n"
                        f"Address: {personalInfo[5]}\n"
                        f"Phone number: {personalInfo[6]}\n\n"
                    )
                    outfile.write(f"{'Course Name:':<20} {'Year:':<6} {'Grade:'}\n")
                    outfile.write("-" * 35 + "\n")
                    for course in courseData:
                        outfile.write(f"{course[0]:<20} {course[1]:<6} {course[2]}\n")

                return jsonify({'message': 'Transcript made successfully'}), 200
            else:
                return jsonify({'message': 'The student does not exist'}), 400

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Get all the students registered for a section
@app.route('/api/students_section', methods=['GET'])
def get_students_in_section():
    try:
        section_id = request.args.get('section_id')
        if section_id == 'No Sections Available For This Course':
            return jsonify({'message': 'There are no Sections available for this course'}), 201

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT registrations.student_id, students.first_name, students.last_name,
                       registrations.section_id, sections.instructor, sections.semester, sections.year
                FROM registrations
                JOIN students ON registrations.student_id = students.student_id
                JOIN sections ON registrations.section_id = sections.section_id
                WHERE registrations.section_id = ?
            """, (section_id,))
            data = cursor.fetchall()

            students_list = [{
                'student_id': row[0],
                'student_name': f"{row[1]} {row[2]}"
            } for row in data]

            section_info = {
                'section_id': data[0][3],
                'instructor': data[0][4],
                'semester': data[0][5],
                'year': data[0][6]
            }

            return jsonify({'students': students_list, 'section': section_info}), 200

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

        section_list = []
        for section in sections:
            section_list.append({
                'section_id': section[0],
                'course_id': section[1],
                'semester': section[2],
                'year': section[3],
                'instructor': section[4],
            })

        return jsonify({'sections': section_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to execute SQL queries
def execute_query(query, params=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Predefined query helper functions
def search_student_by_id(value):
    query = "SELECT * FROM students WHERE student_id = ?"
    return execute_query(query, [value])

def search_student_by_city(value):
    query = "SELECT * FROM students WHERE address LIKE ?"
    return execute_query(query, ['%' + value + '%'])

def search_student_by_zip(value):
    query = "SELECT * FROM students WHERE SUBSTR(address, -5) = ?"
    return execute_query(query, [value])

def search_student_by_email(value):
    query = "SELECT * FROM students WHERE email = ?"
    return execute_query(query, [value])

def search_student_by_first(value):
    query = "SELECT * FROM students WHERE first_name LIKE ?"
    return execute_query(query, ['%' + value + '%'])

def search_student_by_last(value):
    query = "SELECT * FROM students WHERE last_name LIKE ?"
    return execute_query(query, ['%' + value + '%'])

def search_student_by_full(first_name, last_name):
    query = "SELECT * FROM students WHERE first_name LIKE ? AND last_name LIKE ?"
    return execute_query(query, ['%' + first_name + '%', '%' + last_name + '%'])

def search_course_by_id(value):
    query = "SELECT * FROM courses WHERE course_id = ?"
    return execute_query(query, [value])

def search_course_by_rubric(value):
    value = value.upper()
    print(value)
    query = "SELECT * FROM courses WHERE course_id LIKE ?"
    return execute_query(query, ['%' + value + '%'])

def search_course_by_credit(value):
    query = "SELECT * FROM courses WHERE number_credits = ?"
    return execute_query(query, [value])

def search_section_by_id(value):
    query = """
        SELECT sections.*, courses.course_name
        FROM sections
        JOIN courses ON sections.course_id = courses.course_id
        WHERE sections.section_id = ?
    """
    return execute_query(query, [value])

def search_section_by_semester(value):
    query = """
        SELECT sections.*, courses.course_name
        FROM sections
        JOIN courses ON sections.course_id = courses.course_id
        WHERE sections.semester = ?
    """
    return execute_query(query, [value])

def search_section_by_year(value):
    query = """
        SELECT sections.*, courses.course_name
        FROM sections
        JOIN courses ON sections.course_id = courses.course_id
        WHERE sections.year = ?
    """
    return execute_query(query, [value])

def search_section_by_course(value):
    query = """
        SELECT sections.*, courses.course_name
        FROM sections
        JOIN courses ON sections.course_id = courses.course_id
        WHERE sections.course_id = ?
    """
    return execute_query(query, [value])

def search_section_by_instructor(value):
    query = """
        SELECT sections.*, courses.course_name
        FROM sections
        JOIN courses ON sections.course_id = courses.course_id
        WHERE instructor LIKE ?
    """
    return execute_query(query, ['%' + value + '%'])

# Dictionary - maps query options to handler functions
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
    'section_by_id': search_section_by_id,
    'section_by_semester': search_section_by_semester,
    'section_by_year': search_section_by_year,
    'section_by_course': search_section_by_course,
    'section_by_instructor': search_section_by_instructor,
}

# Route for queries
@app.route('/api/search', methods=['POST'])
def query():
    try:
        query_type = request.json.get('optionValue')
        data = {}
        handler = QUERY_HANDLERS.get(query_type)
        if handler:
            if query_type == 'student_by_full':
                first_name = request.json.get('First Name')
                last_name = request.json.get('Last Name')
                data['students'] = handler(first_name, last_name)
            else:
                value = request.json.get('value')
                data_type = query_type.split('_')[0]
                if data_type == 'student':
                    data['students'] = handler(value)
                elif data_type == 'course':
                    data['courses'] = handler(value)
                else:
                    data['sections'] = handler(value)
        else:
            data['error'] = 'Invalid query type'

        print(data)
        return jsonify(data)
    except Exception as e:
        print(f"error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Get courses by student id
@app.route('/api/course_by_student', methods=['GET'])
def get_courses_by_student():
    student_id = request.args.get('student_id')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if not student_id:
        return jsonify({'message': 'Please enter a valid Student ID'})

    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    stud_exist = cursor.fetchone()

    if not stud_exist:
        return jsonify({'message': 'There is no student with that ID'})

    cursor.execute(
        "SELECT registrations.student_id, courses.course_id, courses.course_name, "
        "sections.section_id, sections.semester, sections.year, "
        "students.first_name, students.last_name "
        "FROM registrations "
        "JOIN sections ON registrations.section_id = sections.section_id "
        "JOIN courses ON courses.course_id = sections.course_id "
        "JOIN students ON students.student_id = registrations.student_id "
        "WHERE registrations.student_id = ?", (student_id,)
    )
    registered_courses = cursor.fetchall()
    conn.close()

    course_list = []
    for course in registered_courses:
        entry = {
            'student_id': course[0],
            'course_id': course[1],
            'course_name': course[2],
            'section_id': course[3],
            'semester': course[4],
            'year': course[5],
            'student_name': f"{course[6]} {course[7]}"
        }
        course_list.append(entry)

    return jsonify(course_list)

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
