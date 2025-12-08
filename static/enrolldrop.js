document.addEventListener("DOMContentLoaded", () => {
  const nameEl = document.getElementById("name");
  const usernameEl = document.getElementById("username");



  const enrollCheckbox = document.getElementById("enroll-checkbox");
  const dropCheckbox = document.getElementById("drop-checkbox");
  const courseInput = document.getElementById("course-id");
  const submitBtn = document.getElementById("submit-course");
  const messageEl = document.getElementById("submit-message");

  // Ensure only one checkbox is selected
  enrollCheckbox.addEventListener("change", () => {
    if (enrollCheckbox.checked) dropCheckbox.checked = false;
  });

  dropCheckbox.addEventListener("change", () => {
    if (dropCheckbox.checked) enrollCheckbox.checked = false;
  });

  submitBtn.addEventListener("click", async () => {
    const course_id = courseInput.value.trim();
    const student_id = parseInt(localStorage.getItem("id"));

    if (!course_id) {
      messageEl.style.color = "red";
      messageEl.textContent = "Please enter a course ID.";
      return;
    }

    let action = null;
    if (enrollCheckbox.checked) action = "enroll_class";
    if (dropCheckbox.checked) action = "drop_class";

    if (!action) {
      messageEl.style.color = "red";
      messageEl.textContent = "Select enroll or drop.";
      return;
    }

    try {
      const response = await fetch(`/api/${action}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id, course_id }),
        cache: "no-store"
      });

      const data = await response.json();

      if (data.success) {
        messageEl.style.color = "green";
        messageEl.textContent = `${action === "enroll_class" ? "Enrolled" : "Dropped"} successfully in ${data.course_title}!`;
        courseInput.value = "";
        enrollCheckbox.checked = false;
        dropCheckbox.checked = false;
      } else {
        messageEl.style.color = "red";
        messageEl.textContent = `Error: ${data.message || "Unknown error"}`;
      }
    } catch (err) {
      console.error(err);
      messageEl.style.color = "red";
      messageEl.textContent = "Error sending request.";
    }
  });
});
