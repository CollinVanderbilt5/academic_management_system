document.addEventListener("DOMContentLoaded", () => {
  loadAssignments();
});

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
    warning = `<span class="due-warning">Past due date. Mark complete?</span>`;
  } else if (
    dueDate.toDateString() === now.toDateString()
  ) {
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
      <div><strong>${a.assignment_title}</strong> - <em>${a.course_title}</em></div>
      <div>Due: ${formattedDate} ${highlight} ${warning}</div>
  `;
  return div;
}

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
    container.innerHTML = `<p>Error loading assignments: ${err.message}</p>`;
  }
}
