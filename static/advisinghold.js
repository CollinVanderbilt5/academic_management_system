document.addEventListener("DOMContentLoaded", () => {
  const studentInput = document.getElementById("advise-student-id");
  const swapBtn = document.getElementById("swap-btn");
  const statusSpan = document.getElementById("advise-status");
  const permElem = document.getElementById("username");
  const accountType = localStorage.getItem("account") || "Student";
  permElem.textContent = accountType;

  // Hide the status at first
  statusSpan.parentElement.style.display = "none";
  swapBtn.disabled = true;

  // Create Submit button dynamically
  const submitBtn = document.createElement("button");
  submitBtn.textContent = "Submit";
  submitBtn.classList.add("submit-btn");
  studentInput.parentNode.insertBefore(submitBtn, studentInput.nextSibling);

  // Submit button: check current hold status
  submitBtn.addEventListener("click", async () => {
    const studentID = studentInput.value.trim();
    if (!studentID) {
      alert("Please enter a student ID.");
      return;
    }

    try {
      const response = await fetch("/api/get_hold", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: parseInt(studentID) })
      });

      const data = await response.json();

      if (data.success) {
        statusSpan.textContent = data.advising_hold ? "True" : "False";
        statusSpan.parentElement.style.display = "block"; // show status
        swapBtn.disabled = false; // allow swapping
      } else {
        statusSpan.parentElement.style.display = "block";
        statusSpan.textContent = `Error: ${data.error || "Student not found"}`;
        swapBtn.disabled = true;
      }
    } catch (err) {
      console.error(err);
      alert("Error sending request.");
    }
  });

  // Swap the hold status
swapBtn.addEventListener("click", async () => {
  const studentID = studentInput.value.trim();
  if (!studentID) {
    alert("Please enter a student ID first.");
    return;
  }

  try {
    // Send request to toggle advising hold
    const response = await fetch("/api/edit_hold", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ student_id: parseInt(studentID) })
    });

    const data = await response.json();

    if (data.success) {
      // Fetch the updated hold after swapping
      const updatedResponse = await fetch("/api/get_hold", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: parseInt(studentID) })
      });
      const updatedData = await updatedResponse.json();

      if (updatedData.success) {
        statusSpan.textContent = updatedData.advising_hold ? "True" : "False";
      } else {
        statusSpan.textContent = `Error: ${updatedData.error || "Unknown error"}`;
      }
    } else {
      statusSpan.textContent = `Error: ${data.error || "Unknown error"}`;
    }
  } catch (err) {
    console.error(err);
    alert("Error sending request.");
  }
});

});
