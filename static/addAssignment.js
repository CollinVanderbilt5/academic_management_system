document.addEventListener("DOMContentLoaded", () => {
  const extraFields = document.getElementById("extra-fields");
  const submitBtn = document.getElementById("submit-assignment");

  document.querySelectorAll("input[name='type']").forEach(radio => {
    radio.addEventListener("change", () => {
      extraFields.innerHTML = "";
      const type = radio.value;
      if (type === "Quiz") {
        extraFields.innerHTML = `
          <label>Duration (minutes)</label>
          <input type="number" id="quiz-duration" min="1" />
        `;
      } else if (type === "Exam") {
        extraFields.innerHTML = `
          <label>Room</label>
          <input type="text" id="exam-room" />
        `;
      } else if (type === "Project") {
        extraFields.innerHTML = `
          <label>Number of Group Members</label>
          <input type="number" id="project-partners" min="1" />
        `;
      }
    });
  });

  submitBtn.addEventListener("click", async () => {
    const course_id = parseInt(document.getElementById("assign-course-id").value.trim());
    const title = document.getElementById("assign-title").value.trim();
    const due_date = document.getElementById("assign-due-date").value;
    const description = document.getElementById("assign-desc").value.trim();
    const point_value = parseInt(document.getElementById("assign-points").value.trim());
    const msgBox = document.getElementById("assign-message");
    msgBox.textContent = "";

    const typeRadio = document.querySelector("input[name='type']:checked");
    if (!typeRadio) {
      msgBox.style.color = "red";
      msgBox.textContent = "Please select an assignment type.";
      return;
    }
    const type = typeRadio.value;

    if (!course_id || !title || !due_date || isNaN(point_value)) {
      msgBox.style.color = "red";
      msgBox.textContent = "Please fill out all required fields correctly.";
      return;
    }

    const payload = { course_id, title, description, point_value, due_date, type };

    if (type === "Quiz") {
      const duration = parseInt(document.getElementById("quiz-duration")?.value);
      if (!duration || duration <= 0) {
        msgBox.style.color = "red";
        msgBox.textContent = "Please enter a valid duration for the quiz.";
        return;
      }
      payload.duration = duration;
    } else if (type === "Exam") {
      const room = document.getElementById("exam-room")?.value.trim();
      if (!room) {
        msgBox.style.color = "red";
        msgBox.textContent = "Please enter a room for the exam.";
        return;
      }
      payload.room = room;
    } else if (type === "Project") {
      const partners = parseInt(document.getElementById("project-partners")?.value);
      if (!partners || partners <= 0) {
        msgBox.style.color = "red";
        msgBox.textContent = "Please enter number of group members for the project.";
        return;
      }
      payload.partners = partners;
    }

    try {
      const response = await fetch("/api/add_assignment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (data.success) {
        msgBox.style.color = "green";
        msgBox.textContent = "Assignment added successfully!";
        document.getElementById("assign-course-id").value = "";
        document.getElementById("assign-title").value = "";
        document.getElementById("assign-due-date").value = "";
        document.getElementById("assign-desc").value = "";
        document.getElementById("assign-points").value = "";
        extraFields.innerHTML = "";
      } else {
        msgBox.style.color = "red";
        msgBox.textContent = data.error || "Failed to add assignment. Check course ID.";
      }
    } catch (err) {
      console.error(err);
      msgBox.style.color = "red";
      msgBox.textContent = "Error sending request.";
    }
  });
});
