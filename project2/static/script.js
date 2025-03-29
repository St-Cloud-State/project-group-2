// Array to store student data
const students = [];

// Function to display students in the list
function displayStudents() {
    const studentList = document.getElementById('studentList');
    studentList.innerHTML = ''; // Clear existing student list

    students.forEach(student => {
        const studentElement = document.createElement('div');
        studentElement.innerHTML = `
            <h2>Added Successfully :${student.first_name} ${student.last_name}</h2>
        `;
        studentList.appendChild(studentElement);
    });
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

        .then(response => response.json())
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
    });
}

// Attach the addStudent function to the form submit event
document.getElementById('studentForm').addEventListener('submit', addStudent);


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

