// ---------------- STEP 1: Program Start ----------------
console.log("----- STUDENT PERFORMANCE ANALYZER -----");

// ---------------- STEP 2: Student Data ----------------
const students = [
  {
    name: "Lalit",
    marks: [
      { subject: "Math", score: 78 },
      { subject: "English", score: 82 },
      { subject: "Science", score: 74 },
      { subject: "History", score: 69 },
      { subject: "Computer", score: 88 },
    ],
    attendance: 82,
  },
  {
    name: "Rahul",
    marks: [
      { subject: "Math", score: 90 },
      { subject: "English", score: 85 },
      { subject: "Science", score: 80 },
      { subject: "History", score: 76 },
      { subject: "Computer", score: 92 },
    ],
    attendance: 91,
  },
];

console.log("\nStep 1: Student Data Loaded");

// ---------------- STEP 3: Total Marks ----------------
function calculateTotal(student) {
  let total = 0;
  for (let i = 0; i < student.marks.length; i++) {
    total += student.marks[i].score;
  }
  return total;
}

console.log("\nStep 2: Total Marks");
students.forEach((student) => {
  console.log(`${student.name} Total Marks: ${calculateTotal(student)}`);
});

// ---------------- STEP 4: Average Marks ----------------
function calculateAverage(student) {
  return calculateTotal(student) / student.marks.length;
}

console.log("\nStep 3: Average Marks");
students.forEach((student) => {
  console.log(`${student.name} Average: ${calculateAverage(student)}`);
});

// ---------------- STEP 5: Subject Highest ----------------
console.log("\nStep 4: Subject-wise Highest");

function getHighestBySubject(students) {
  const subjects = students[0].marks.map((m) => m.subject);

  subjects.forEach((subject) => {
    let highest = 0;
    let topper = "";

    students.forEach((student) => {
      const data = student.marks.find((m) => m.subject === subject);

      if (data.score > highest) {
        highest = data.score;
        topper = student.name;
      }
    });

    console.log(`Highest in ${subject}: ${topper} (${highest})`);
  });
}

getHighestBySubject(students);

// ---------------- STEP 6: Subject Average ----------------
console.log("\nStep 5: Subject-wise Average");

function getSubjectAverage(students) {
  const subjects = students[0].marks.map((m) => m.subject);

  subjects.forEach((subject) => {
    let total = 0;

    students.forEach((student) => {
      const data = student.marks.find((m) => m.subject === subject);
      total += data.score;
    });

    console.log(`Average ${subject}: ${total / students.length}`);
  });
}

getSubjectAverage(students);

// ---------------- STEP 7: Topper ----------------
console.log("\nStep 6: Class Topper");

function getTopper(students) {
  let highest = 0;
  let topper = "";

  students.forEach((student) => {
    const total = calculateTotal(student);

    if (total > highest) {
      highest = total;
      topper = student.name;
    }
  });

  console.log(`Class Topper: ${topper} with ${highest} marks`);
}

getTopper(students);

// ---------------- STEP 8: Grade ----------------
console.log("\nStep 7: Grades");

function getGrade(student) {
  const avg = calculateAverage(student);

  const failedSubject = student.marks.find((m) => m.score <= 40);

  if (student.attendance < 75) {
    return "Fail (Low Attendance)";
  }

  if (failedSubject) {
    return `Fail (Failed in ${failedSubject.subject})`;
  }

  if (avg >= 85) return "A";
  if (avg >= 70) return "B";
  if (avg >= 50) return "C";

  return "Fail";
}

students.forEach((student) => {
  console.log(`${student.name} Grade: ${getGrade(student)}`);
});

// ---------------- STEP 9: Final Report ----------------
console.log("\nStep 8: Final Report");

students.forEach((student) => {
  console.log("\n----------------------");
  console.log(`Name: ${student.name}`);
  console.log(`Total: ${calculateTotal(student)}`);
  console.log(`Average: ${calculateAverage(student)}`);
  console.log(`Grade: ${getGrade(student)}`);
});
