<<<<<<< HEAD
// addAssignment.js

// Parse a YYYY-MM-DD string as a local date to avoid timezone issues
function parseLocalDate(raw) {
  if (!raw) return null;
  const [year, month, day] = raw.split("-").map(Number);
  return new Date(year, month - 1, day);
}

// Format date for display
function formatDate(raw) {
  const date = parseLocalDate(raw);
  if (!date) return "No date";

  const now = new Date();
  const oneWeekFromNow = new Date();
  oneWeekFromNow.setDate(now.getDate() + 7);

  let warning = "";
  let highlight = "";

  if (date < now) {
    warning = `<span class="due-warning">Past due date. Mark complete?</span>`;
  } else if (
    date.getDate() === now.getDate() &&
    date.getMonth() === now.getMonth() &&
    date.getFullYear() === now.getFullYear()
  ) {
    highlight = `<span class="highlight">Due Today</span>`;
  } else if (date < oneWeekFromNow) {
    highlight = `<span class="highlight">Due This Week</span>`;
  }

  return `${date.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric"
  })} ${highlight} ${warning}`;
}

// Render a single assignment box
function renderAssignment(a) {
  const div = document.createElement("div");
  div.classList.add("assignment-box");

  const formattedDate = formatDate(a.due_date);

  div.innerHTML = `
      <div><strong>${a.title}</strong></div>
      <div>Due: ${formattedDate}</div>
  `;

  return div;
}

// Load assignments from backend
async function loadAssignments() {
  const container = document.getElementById("assignments-container");
  container.innerHTML = "Loading...";

  try {
    const response = await fetch("/api/get_assignments");
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const data = await response.json();

    if (!data.success || !data.assignments || data.assignments.length === 0) {
      container.innerHTML = "<p>No assignments found.</p>";
      return;
    }

    container.innerHTML = "";
    data.assignments.forEach(assign => {
      const box = renderAssignment(assign);
      container.appendChild(box);
    });
  } catch (err) {
    console.error("Error fetching assignments:", err);
    container.innerHTML = "<p>Error loading assignments.</p>";
  }
}

// Populate user info in header
function populateUserInfo() {
  const nameElem = document.getElementById("name");
  const permElem = document.getElementById("username");

  const userName = localStorage.getItem("name");
  const accountType = localStorage.getItem("account");

  if (nameElem) nameElem.textContent = userName || "John Doe";
  if (permElem) permElem.textContent = accountType || "Student";
}

// Main DOM logic
document.addEventListener("DOMContentLoaded", () => {
  populateUserInfo();

  const btn = document.getElementById("submit-assignment");
  if (!btn) return;

  btn.addEventListener("click", async () => {
    const course_id = parseInt(document.getElementById("assign-course-id").value.trim());
    const title = document.getElementById("assign-title").value.trim();
    const due_date_input = document.getElementById("assign-due-date").value;
    const description = document.getElementById("assign-desc").value.trim();

    const msgBox = document.getElementById("assign-message");
    msgBox.textContent = ""; // clear old messages

    if (!course_id || isNaN(course_id) || !title || !due_date_input) {
      msgBox.style.color = "red";
      msgBox.textContent = "Please fill out all required fields correctly.";
      return;
    }

    try {
      const response = await fetch("/api/add_assignment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          course_id,
          title,
          description,
          point_value: 0,
          due_date: due_date_input
        })
      });

      const data = await response.json();

      if (data.success) {
        msgBox.style.color = "green";
        msgBox.textContent = "Assignment added successfully!";

        // Clear fields
        document.getElementById("assign-course-id").value = "";
        document.getElementById("assign-title").value = "";
        document.getElementById("assign-due-date").value = "";
        document.getElementById("assign-desc").value = "";

        loadAssignments(); // refresh calendar
      } else {
        msgBox.style.color = "red";
        msgBox.textContent = "Failed to add assignment. Check course ID.";
      }
    } catch (err) {
      console.error(err);
      msgBox.style.color = "red";
      msgBox.textContent = "Error sending request.";
    }
  });

  loadAssignments(); // initial load
});
=======
// addAssignment.js

// Parse a YYYY-MM-DD string as a local date to avoid timezone issues
function parseLocalDate(raw) {
  if (!raw) return null;
  const [year, month, day] = raw.split("-").map(Number);
  return new Date(year, month - 1, day);
}

// Format date for display
function formatDate(raw) {
  const date = parseLocalDate(raw);
  if (!date) return "No date";

  const now = new Date();
  const oneWeekFromNow = new Date();
  oneWeekFromNow.setDate(now.getDate() + 7);

  let warning = "";
  let highlight = "";

  if (date < now) {
    warning = `<span class="due-warning">Past due date. Mark complete?</span>`;
  } else if (
    date.getDate() === now.getDate() &&
    date.getMonth() === now.getMonth() &&
    date.getFullYear() === now.getFullYear()
  ) {
    highlight = `<span class="highlight">Due Today</span>`;
  } else if (date < oneWeekFromNow) {
    highlight = `<span class="highlight">Due This Week</span>`;
  }

  return `${date.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric"
  })} ${highlight} ${warning}`;
}

// Render a single assignment box
function renderAssignment(a) {
  const div = document.createElement("div");
  div.classList.add("assignment-box");

  const formattedDate = formatDate(a.due_date);

  div.innerHTML = `
      <div><strong>${a.title}</strong></div>
      <div>Due: ${formattedDate}</div>
  `;

  return div;
}

// Load assignments from backend
async function loadAssignments() {
  const container = document.getElementById("assignments-container");
  container.innerHTML = "Loading...";

  try {
    const response = await fetch("/api/get_assignments");
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const data = await response.json();

    if (!data.success || !data.assignments || data.assignments.length === 0) {
      container.innerHTML = "<p>No assignments found.</p>";
      return;
    }

    container.innerHTML = "";
    data.assignments.forEach(assign => {
      const box = renderAssignment(assign);
      container.appendChild(box);
    });
  } catch (err) {
    console.error("Error fetching assignments:", err);
    container.innerHTML = "<p>Error loading assignments.</p>";
  }
}

// Populate user info in header
function populateUserInfo() {
  const nameElem = document.getElementById("name");
  const permElem = document.getElementById("username");

  const userName = localStorage.getItem("name");
  const accountType = localStorage.getItem("account");

  if (nameElem) nameElem.textContent = userName || "John Doe";
  if (permElem) permElem.textContent = accountType || "Student";
}

// Main DOM logic
document.addEventListener("DOMContentLoaded", () => {
  populateUserInfo();

  const btn = document.getElementById("submit-assignment");
  if (!btn) return;

  btn.addEventListener("click", async () => {
    const course_id = parseInt(document.getElementById("assign-course-id").value.trim());
    const title = document.getElementById("assign-title").value.trim();
    const due_date_input = document.getElementById("assign-due-date").value;
    const description = document.getElementById("assign-desc").value.trim();

    const msgBox = document.getElementById("assign-message");
    msgBox.textContent = ""; // clear old messages

    if (!course_id || isNaN(course_id) || !title || !due_date_input) {
      msgBox.style.color = "red";
      msgBox.textContent = "Please fill out all required fields correctly.";
      return;
    }

    try {
      const response = await fetch("/api/add_assignment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          course_id,
          title,
          description,
          point_value: 0,
          due_date: due_date_input
        })
      });

      const data = await response.json();

      if (data.success) {
        msgBox.style.color = "green";
        msgBox.textContent = "Assignment added successfully!";

        // Clear fields
        document.getElementById("assign-course-id").value = "";
        document.getElementById("assign-title").value = "";
        document.getElementById("assign-due-date").value = "";
        document.getElementById("assign-desc").value = "";

        loadAssignments(); // refresh calendar
      } else {
        msgBox.style.color = "red";
        msgBox.textContent = "Failed to add assignment. Check course ID.";
      }
    } catch (err) {
      console.error(err);
      msgBox.style.color = "red";
      msgBox.textContent = "Error sending request.";
    }
  });

  loadAssignments(); // initial load
});
>>>>>>> 1d3f5a584e2b2700cde815592feb624578faa31b
