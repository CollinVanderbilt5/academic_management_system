document.addEventListener("DOMContentLoaded", () => {
  loadAssignments();
  const permElem = document.getElementById("username");
  const accountType = localStorage.getItem("account") || "Student";
  permElem.textContent = accountType;

  // Setup filter checkbox listeners
  document.getElementById("filter-today").addEventListener("change", applyFilters);
  document.getElementById("filter-week").addEventListener("change", applyFilters);

  // Setup search listeners
  document.getElementById("search-name").addEventListener("input", applyFilters);
  document.getElementById("search-course").addEventListener("input", applyFilters);

  // Setup sort listeners
  document.getElementById("sort-date").addEventListener("change", applyFilters);
  document.getElementById("sort-class").addEventListener("change", applyFilters);
});

let ALL_ASSIGNMENTS = [];

function renderAssignment(a) {
  const div = document.createElement("div");
  div.classList.add("assignment-box");

  const dueDate = new Date(a.due_date);
  const now = new Date();
  const oneWeekFromNow = new Date();
  oneWeekFromNow.setDate(now.getDate() + 7);

  let warning = "";
  let highlight = "";

  if (dueDate < now) {
    warning = `<span class="due-warning">Past due date.</span>`;
  } else if (dueDate.toDateString() === now.toDateString()) {
    highlight = `<span class="highlight">Due Today</span>`;
  } else if (dueDate < oneWeekFromNow) {
    highlight = `<span class="highlight">Due This Week</span>`;
  }

  const formattedDate = dueDate.toLocaleDateString(undefined, {
    weekday: "long",
    month: "long",
    day: "numeric"
  });

  div.innerHTML = `
      <input type="checkbox" class="complete-checkbox" data-course="${a.course_id}" data-title="${a.assignment_title}" />
      <div><strong>${a.assignment_title}</strong> - <em>${a.course_title}</em></div>
      <div>Due: ${formattedDate} ${highlight} ${warning}</div>
  `;

  // Add listener for checkmark
  const checkbox = div.querySelector(".complete-checkbox");
  checkbox.addEventListener("change", () => markComplete(a.course_id, a.assignment_title, div));

  return div;
}

async function markComplete(courseId, assignmentTitle, div) {
  try {
    const response = await fetch("/api/complete_assignment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ course_id: courseId, title: assignmentTitle })
    });
    const result = await response.json();

    if (result.success) {
      // Remove from the displayed list
      div.remove();

      // Update ALL_ASSIGNMENTS so it doesn't show up on next filter
      ALL_ASSIGNMENTS = ALL_ASSIGNMENTS.filter(a => !(a.course_id === courseId && a.assignment_title === assignmentTitle));
    } else {
      alert("Error marking assignment complete: " + result.error);
    }
  } catch (err) {
    console.error("Error marking assignment complete:", err);
  }
}

async function loadAssignments() {
  const container = document.getElementById("assignments-container");
  container.innerHTML = "Loading...";

  try {
    const response = await fetch("/api/get_assignments");
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const data = await response.json();
    if (!data.success || !data.assignments) {
      container.innerHTML = "<p>No assignments found.</p>";
      return;
    }

    // Only include assignments that are not completed
    ALL_ASSIGNMENTS = data.assignments.filter(a => !a.completed);

    applyFilters();

  } catch (err) {
    console.error("Error fetching assignments:", err);
    container.innerHTML = `<p>Error loading assignments: ${err.message}</p>`;
  }
}

function applyFilters() {
  const container = document.getElementById("assignments-container");
  container.innerHTML = "";

  let list = [...ALL_ASSIGNMENTS];

  const todayChecked = document.getElementById("filter-today").checked;
  const weekChecked = document.getElementById("filter-week").checked;
  const searchName = document.getElementById("search-name").value.toLowerCase();
  const searchCourse = document.getElementById("search-course").value.toLowerCase();
  const sortDate = document.getElementById("sort-date").checked;
  const sortClass = document.getElementById("sort-class").checked;

  const now = new Date();
  const oneWeekFromNow = new Date();
  oneWeekFromNow.setDate(now.getDate() + 7);

  // Filters
  if (todayChecked) list = list.filter(a => new Date(a.due_date).toDateString() === now.toDateString());
  if (weekChecked) list = list.filter(a => { const d = new Date(a.due_date); return d >= now && d < oneWeekFromNow; });
  if (searchName) list = list.filter(a => a.assignment_title.toLowerCase().includes(searchName));
  if (searchCourse) list = list.filter(a => a.course_id.toLowerCase().includes(searchCourse) || a.course_title.toLowerCase().includes(searchCourse));

  // Sorts
  if (sortDate) list.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
  if (sortClass) list.sort((a, b) => a.course_title.localeCompare(b.course_title));

  if (list.length === 0) {
    container.innerHTML = "<p>No assignments match your filters/search.</p>";
    return;
  }

  list.forEach(a => container.appendChild(renderAssignment(a)));
}
