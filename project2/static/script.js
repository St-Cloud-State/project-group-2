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

//Register a student to a course
function registerStudent(event){
    event.preventDefault();
    const formData = new FormData(document.getElementById('registerForm'));

    //Registration Object
    const registrationData = {
        section_ID: document.getElementById('section_ID').value,
        student_ID: formData.get('student_ID')
    };

    fetch('/api/registerStudent',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(registrationData)

    })

    .then(response =>response.json()) 
    .then(data =>{
        console.log(data.message);
        //Sends the alert message upon success
        alert(data.message);
    })
    .catch(error =>{
        console.error('Error registering student', error);
        alert(error.message);
    });
    
}
document.getElementById('registerForm').addEventListener('submit', registerStudent);

//Add a grade to student's section
function addGrade(event){
    event.preventDefault();
    const formData = new FormData(document.getElementById('addGradeForm'));

    //Registration Object
    const registrationData = {
        section_ID: formData.get('section_ID'),
        student_ID: formData.get('student_ID'),
        grade:  formData.get('grade')
    };

    fetch('/api/addGrade',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(registrationData)

    })

    .then(response => {
        if (!response.ok){
            return response.json().then(data =>{
                throw new Error(data.message);
            })
        }
        return response.json();
            
    })

    .then(data =>{
        console.log(data.message);
        //Sends the alert message upon success
        alert(data.message);
    })
    .catch(error =>{
        console.error('Error adding grade', error);
        alert(error.message);
    });
    
}
document.getElementById('addGradeForm').addEventListener('submit', addGrade);

//Print a student's transcript
function printTranscript(event){
    event.preventDefault();

    const formData = new FormData(document.getElementById('printTranscriptForm'));

    const transcriptData ={
        student_ID: formData.get('student_ID')
    };

    fetch('/api/printTranscript',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(transcriptData)

    })

    .then(response =>response.json()) 

    .then(data =>{
        console.log(data.message);
        //Sends the alert message upon success
        alert(data.message);
    })
    .catch(error =>{
        console.error('Error printing transcript', error);
        alert(error.message);
    });

}
document.getElementById('printTranscriptForm').addEventListener('submit', printTranscript);


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

// Map of predefined query options
const queryMap = {
    students: [
        { label: "Find Student by ID", value: "student_by_id", needsInput: true },
        { label: "Find Students by City", value: "student_by_city", needsInput: true },
        { label: "Find Students by Zipcode", value: "student_by_zip", needsInput: true },
        { label: "Find Students by Email", value: "student_by_email", needsInput: true },
        { label: "Find Students by First Name", value: "student_by_first", needsInput: true },
        { label: "Find Students by Last Name", value: "student_by_last", needsInput: true },
        { label: "Find Student by Full Name", value: "student_by_full", needsInput: ["First Name", "Last Name"] }
    ],  
    
    courses: [
        { label: "Find Course by ID", value: "course_by_id", needsInput: true },
        { label: "List Courses with specific Rubric", value: "course_by_rubric", needsInput: true },
        { label: "List Courses with specific number of credits", value: "course_by_credit", needsInput: true },
    ],

    sections: [
        { label: "Find Section by ID", value: "section_by_id", needsInput: true },
        { label: "List Sections offered in a specific semester", value: "section_by_semester", needsInput: true },
        { label: "List Sections offered in a specific year", value: "section_by_year", needsInput: true },
        { label: "List Sections of a Course", value: "section_by_course", needsInput: true },
        { label: "List Sections with a specified Instructor", value: "section_by_instructor", needsInput: true },
        
    ]
}

// Change listenter - for when a selection is changed in the dropdown
document.getElementById('queryTable').onchange = queryOptions;
queryOptions.call(document.getElementById('queryTable'));

// Function to update the query options dropdown
function queryOptions() {
    const table = this.value;
    console.log(table);

    let str = "";
    //console.log(queryMap[table]);

    queryMap[table].forEach(query => {
    
        str += "<option>" + query.label + "</option>"
    })
        
    
    document.getElementById('queryOptions').innerHTML = str;
    inputFields();
}

// Change listener
document.getElementById('queryOptions').onchange = inputFields;

// Function to dynamically add or remove text input based on query selection
function inputFields() {
    const selectedQuery = document.getElementById('queryOptions').value;
    const table = document.getElementById('queryTable').value;
    const queryParamContainer = document.getElementById('queryParamContainer');

    // Clear inputs
    queryParamContainer.innerHTML = "";

    // Find the correct query in the map
    const selectedQueryOption = queryMap[table].find(q => q.label === selectedQuery);
    console.log(selectedQueryOption);
    if (selectedQueryOption.needsInput) {
        if(Array.isArray(selectedQueryOption.needsInput)) {

            // Create multiple input fields 
            selectedQueryOption.needsInput.forEach(field => {
                const label = document.createElement("label");
                label.innerText = `Enter ${field}:`;
                
                const input = document.createElement("input");
                input.type = field === "year" ? "number" : "text";
                input.id = field;
                input.placeholder = `Enter ${field}`;
                input.required = true;
                
                if (field === "zipcode") {
                    input.pattern = "[0-9]{5}";
                    input.title = "Enter a valid 5-digit zipcode";
                    input.required = true;
                }
                queryParamContainer.appendChild(label);
                queryParamContainer.appendChild(input);
                queryParamContainer.appendChild(document.createElement("br")); // Add spacing
       

            });
        } else {
            
            // One input
            const input = document.createElement("input");
            input.type = "text";
            input.id = "queryParam";
            input.placeholder = "Enter query term";
            queryParamContainer.appendChild(input);
        }
    }
}

// Function to make the query
function search() {
    
    const table = document.getElementById('queryTable').value;
    const optionLabel = document.getElementById('queryOptions').value;
    const optionValue = queryMap[table].find(query => query.label === optionLabel).value;
    var requestData = { optionValue };

    // Find the selected query option in the query map
    const selectedQueryOption = queryMap[table].find(q => q.label === optionLabel);

    if (selectedQueryOption.needsInput) {
        if (Array.isArray(selectedQueryOption.needsInput)) {
            // Get multiple input values
            selectedQueryOption.needsInput.forEach(field => {
                
                requestData[field] = document.getElementById(field).value.trim();
                })    
        } else {
            // single input
            requestData.value = document.getElementById('queryParam').value.trim();
        }
    }

    console.log("Request: ", requestData);

    fetch('/api/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        const results = document.getElementById('queryResults');
        results.innerHTML = ''; // Clear previous results

        // Check the response data
        // if the data is student data and is not empty   
        if(data.students && data.students.length) {
            data.students.forEach(student => {
                console.log(data.students[0]);
                const studentElement = document.createElement('div');
                studentElement.innerHTML = `
                    <h2>${student[1]} ${student[2]}</h2>
                    <p>Student ID: ${student[0]}</p>
                    <p>DOB: ${student[3]}</p>
                    <p>Email: ${student[4]}</p>
                    <p>Adress: ${student[5]}</p>
                `;
                results.appendChild(studentElement);
            });
        } else if (data.courses && data.courses.length) {
            data.courses.forEach(course => {
                const courseElement = document.createElement('div');
                courseElement.innerHTML = `
                    <h2>${course[0]} ${course[1]}</h2>
                    <p>Course Description: ${course[2]}</p>
                    <p>Credits: ${course[3]}</p>
                `;
                results.appendChild(courseElement);
            });
        } else if (data.sections && data.sections.length) {
            
            data.sections.forEach(section => {
                const sectionElement = document.createElement('div');
                sectionElement.innerHTML = `
                <h2>${section[5]}</h2>    
                    <h3>Section ID: ${section[0]}</h3>
                        <p>Course ID: ${section[1]}</p>
                        <p>Semester: ${section[2]}</p>
                        <p>Year: ${section[3]}</p>
                        <p>Instructor: ${section[4]}</p>
            `;
            results.appendChild(sectionElement);
        });
        } else {
            // no data found
            results.innerHTML = '<p>No results found for the query.</p>';
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        alert('An error occurred while searching for data.');
        });
}


// Put the list of courses in the drop down
document.getElementById('register_course_id').onchange = sectionDropDown;

courseDropDown.call(document.getElementById('register_course_id'));


function courseDropDown() {
    fetch('api/courses')
        .then(response => response.json())
        .then(data => {
            let str = "<option>>-- Select a Course --<</option>";
            data.courses.forEach(course => {
                str += "<option>" + course.course_id + "</option>"
            });

            document.getElementById('register_course_id').innerHTML = str;
        })
        .catch(error => console.error("Error fetching courses", error));
        sectionDropDown();
}


// Put the sections of the selected course in the drop down
function sectionDropDown() {
    const courseId = document.getElementById('register_course_id').value;
    fetch(`api/search_sections?course_id=${courseId}`)
        .then(response => response.json())
        .then(data => {
            let str = "";
            
            if (data.sections && data.sections.length) {
                data.sections.forEach(section => {
                    str += "<option>" + section.section_id + " - " + section.semester + " - " + section.year + "</option>"
                });
            }
            else {
                str += "<option>No Sections Available For This Course</option>";
            }
            

            document.getElementById('section_ID').innerHTML = str;
        })
        .catch(error => console.error("Error fetching sections", error));

}



availCourseDropDown.call(document.getElementById('avail_courses'));
document.getElementById('avail_courses').onchange = availSectionDropDown;

function availCourseDropDown() {
    fetch('api/courses')
        .then(response => response.json())
        .then(data => {
            let str = "<option>>-- Select a Course --<</option>";
            data.courses.forEach(course => {
                str += "<option>" + course.course_id + "</option>"
            });

            document.getElementById('avail_courses').innerHTML = str;
        })
        .catch(error => console.error("Error fetching courses", error));
        availSectionDropDown();
}



// Put the sections of the selected course in the drop down
function availSectionDropDown() {
    const courseId = document.getElementById('avail_courses').value;
    fetch(`api/search_sections?course_id=${courseId}`)
        .then(response => response.json())
        .then(data => {
            let str = "";
            
            if (data.sections && data.sections.length) {
                data.sections.forEach(section => {
                    str += "<option>" + section.section_id + " - " + section.semester + " - " + section.year + "</option>"
                });
            }
            else {
                str += "<option>No Sections Available For This Course</option>";
            }
            

            document.getElementById('avail_sections').innerHTML = str;
        })
        .catch(error => console.error("Error fetching sections", error));

}

function showStudentReg(){
    const studentId = document.getElementById('reg_student_id').value.trim();

    fetch(`api/course_by_student?student_id=${studentId}`)
        .then(response => response.json())
        .then(data => {
            const results = document.getElementById('student_registered_list');
            results.innerHTML = ''; // Clear previous results
            if(data && data.length) {
                results.innerHTML = `<h2>Course List for: ${data[0].student_name}</h2>`;
                data.forEach(course => {
                    const courseElement = document.createElement('div');
                    courseElement.innerHTML = `
                    <h3>${course.course_id} ${course.course_name}</h3>
                        <p>Section ID: ${course.section_id}</p>
                        <p>Semester: ${course.semester}</p>
                        <p>Year: ${course.year}</p>
                        <hr>
                    `;
                    results.appendChild(courseElement);
                })
            } else {
                // no data found
                results.innerHTML = '<p>This student is not registered for any courses</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching course data:', error);
        });

}

function studentsInSection() {
    const sectionId = document.getElementById('avail_sections').value.split(" ")[0];
    
    const courseId = document.getElementById('avail_courses').value;
    fetch(`api/students_section?section_id=${sectionId}`)
        .then(response => response.json())
        .then(data => {
            const results = document.getElementById('students_in_section');
            results.innerHTML = '';
            if (data.students && data.students.length) {
                results.innerHTML = `
                <h2>Student List for: ${courseId} - ${data.section.section_id}</h2><br>
                <h3>Instructor: ${data.section.instructor}</h3>
                <h3>Semester: ${data.section.semester} ${data.section.year}</h3><hr>
                <h4>Student Name (Student ID)</h4>
                `;

                let i = 1;
                data.students.forEach(student => {
                    const sectionElement = document.createElement('div');
                    sectionElement.innerHTML = `<h4>${i}: ${student.student_name} (${student.student_id})</h4>`;
                    i++;
                    results.appendChild(sectionElement);
                })

                results.appendChild(document.createElement('hr'));
            } else {
                results.innerHTML = `<p>No students are registered for this section</p>`;
            }
        })
        .catch(error => {
            console.error('Error fetching student/section data', error);
        })
}