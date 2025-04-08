// Array to store student data
const students = [];
const courses = [];
const sections = [];

// Function to display students in the list
function displayStudents() {
    const studentList = document.getElementById('studentList');
    studentList.innerHTML = ''; // Clear existing student list

    students.forEach(student => {
        const studentElement = document.createElement('div');
        studentElement.innerHTML = `
            <h2>Added Successfully: ${student.first_name} ${student.last_name}</h2>
        `;
        studentList.appendChild(studentElement);
    });
}

// Function to display courses in the list
function displayCourses() {
    const courseList = document.getElementById('courseList');
    courseList.innerHTML = ''; // Clear existing course list

    courses.forEach(course => {
        const courseElement = document.createElement('div');
        courseElement.innerHTML = `
            <h2>Added Successfully: ${course.course_id} ${course.course_name}</h2>
        `;
        courseList.appendChild(courseElement);
    })
}

//Function to display sections as they are added
function displaySections(){
    const sectionList = document.getElementById('sectionList');
    sectionList.innerHTML = ''; //Clear existing section list

    sections.forEach(section =>{
        const sectionElement = document.createElement('div');
        sectionElement.innerHTML = `
        <h2>Section for ${section.course_id} added successfully</h2>
        `;
        sectionList.appendChild(sectionElement);
    })
}


// Add Student
function addStudent(event) {
    
    // Prevent form from submitting default 
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(document.getElementById('studentForm'));
    
    // Combine the parts of the address into one full address to be compliant with the DB
    const city = formData.get('city');
    const state = formData.get('state');
    const zip = formData.get('zip');
    const address = formData.get('address');

    const fullAddress = `${address} ${city} ${state} ${zip}`;

    // Make student data object
    const studentData = {
        first_name: formData.get('firstName'),
        last_name: formData.get('lastName'),
        dob: formData.get('dob'),
        email: formData.get('email'),
        address: fullAddress,
        phone: formData.get('phone')
    };

    // Send to backend
    fetch('/api/add_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(studentData)
    })

        .then(response => {
            if(!response.ok){
                return response.json().then(data => {
                    throw new Error(data.message);
                })
            }
            
            return response.json;
        })
        .then(data => {
            // Display a success message or handle errors if needed
            console.log(data.message);

            // Add the new student data to the student array
            students.push(studentData);
            console.log(students)

            // Clear the form
            document.getElementById('studentForm').reset();

            // Refresh the student list
            displayStudents();
    })
    .catch(error => {
        console.error('Error adding student:', error);
        alert(error.message);
    });
}
// Attach the addStudent function to the form submit event
document.getElementById('studentForm').addEventListener('submit', addStudent);


// Add course
function addCourse(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('courseForm'));

    // Combine rubric and course number to form the primary key
    const rubric = formData.get('rubric');
    const course_number = formData.get('course_number');
    const course_id = `${rubric}${course_number}`;

    // Make course object
    const courseData = {
        course_id: course_id,
        course_name: formData.get('course_name'),
        course_description: formData.get('course_description'),
        number_credits: formData.get('number_credits')
    };

    // Send to backend
    fetch('/api/add_course', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(courseData)
    })

    .then(response => {
        if (!response.ok){
            return response.json().then(data => {
                throw new Error(data.message);
            })
        }
        return response.json;
    })
    .then(data => {

        console.log(data.message);
        courses.push(courseData);
        console.log(courses);

        // clear the form
        document.getElementById('courseForm').reset();

        displayCourses();
    })
    .catch(error => {
        console.error('Error adding course', error);
        alert(error.message);
    });
}

// add the listener
document.getElementById('courseForm').addEventListener('submit', addCourse);

//Add section
function addSection(event){
    event.preventDefault();
    const formData = new FormData(document.getElementById('sectionForm'));

    //Make section data object
    const sectionData = {
        course_id:  formData.get('course_ID'),
        semester: formData.get('semester'),
        year:   formData.get('year'),
        instructor: formData.get('instructor')

    };

    //Send data to backend
    fetch('/api/add_section', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(sectionData)
    })

        .then(response => {
            if (!response.ok){
                return response.json().then(data =>{
                    throw new Error(data.message);
                })
            }
            return response.json;
                //throw new Error(data.message);
        })
        .then(data => {
            console.log(data.message);

            sections.push(sectionData);
            console.log(sections)
            document.getElementById('sectionForm').reset();
            
            displaySections();
            
        })
        .catch(error => {
            console.error('Error adding sections:', error);
            alert(error.message);
        });
}

document.getElementById('sectionForm').addEventListener('submit', addSection);

// Function to fetch and display all students from the server
function showAllStudents() {
    fetch('/api/students')
        .then(response => response.json())
        .then(data => {
            const studentList = document.getElementById('allstudents');
            studentList.innerHTML = ''; // Clear existing student list
            console.log(data)
            data.students.forEach(student => { // Access the 'students' key in the JSON response
                const studentElement = document.createElement('div');
                studentElement.innerHTML = `
                    <h2>${student.first_name} ${student.last_name}</h2>
                    <p>DOB: ${student.date_of_birth}</p>
                    <p>Email: ${student.email}</p>
                `;
                studentList.appendChild(studentElement);
            });
        })
        .catch(error => {
            console.error('Error fetching all students:', error);
        });
}

// Function to fetch and display all courses
function showAllCourses() {
    fetch('/api/courses')
        .then(response => response.json())
        .then(data => {
            const courseList = document.getElementById('allstudents');
            courseList.innerHTML = ''; // clear the list
            
            console.log(data);

            data.courses.forEach(course => {
                const courseElement = document.createElement('div');
                courseElement.innerHTML = `
                    <h2>${course.course_id} ${course.course_name}</h2>
                    <p>Description: ${course.course_description}</p>
                    <p>Credits: ${course.number_credits}</p>
                `;
                courseList.appendChild(courseElement);
            });
         
        })
        .catch(error => {
            console.error('Error fetching courses', error)
        });
}

// Function to search for course sections
function searchSections() {
    const courseID = document.getElementById('searchCourseID').value.trim();

    if (!courseID) {
        alert("Please enter a Course ID.");
        return;
    }

    fetch(`/api/search_sections?course_id=${courseID}`)
        .then(response => response.json())
        .then(data => {
            const sectionList = document.getElementById('sectionList');
            sectionList.innerHTML = ''; // Clear previous results

            if (data.sections && data.sections.length > 0) {
                data.sections.forEach(section => {
                    const sectionElement = document.createElement('div');
                    sectionElement.innerHTML = `
                        <h3>Section ID: ${section.section_id}</h3>
                        <p>Course ID: ${section.course_id}</p>
                        <p>Semester: ${section.semester}</p>
                        <p>Year: ${section.year}</p>
                        <p>Instructor: ${section.instructor}</p>
                        <hr>
                    `;
                    sectionList.appendChild(sectionElement);
                });
            } else {
                sectionList.innerHTML = '<p>No sections found for the given Course ID.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching sections:', error);
            alert('An error occurred while searching for sections.');
        });
}