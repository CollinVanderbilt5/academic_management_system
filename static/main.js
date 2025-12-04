document.addEventListener("DOMContentLoaded", () => {
  const username = localStorage.getItem("name");
  const user_id = localStorage.getItem("id");
  const data = localStorage.getItem("BackendData")

  console.log("localStorage contents:", localStorage);

  if (username) { 
    document.getElementById('name').innerText = "Hello " + username + "!";
  }
    const loginForm = document.getElementById("login-form");

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const messageEl = document.getElementById("login-message");

      try {
        const response = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        });

        const result = await response.json();

        if (result.success) {
          const userID = result.user.id;
          const userName = result.user.name;

          localStorage.setItem("userID", userID);
          localStorage.setItem("userName", userName || "");

          messageEl.style.color = "green";
          messageEl.innerText = `Welcome, ${userName}! Redirecting...`;

          setTimeout(() => {
            window.location.href = "/homepage";
          }, 600);
        } else {
          messageEl.style.color = "red";
          messageEl.innerText = result.message || "Login failed.";
        }
      } catch (error) {
        messageEl.style.color = "red";
        messageEl.innerText = "Server error.";
        console.error(error);
      }
    });
  }

  const nameEl = document.getElementById("name");
  const usernameEl = document.getElementById("username");
  const classListEl = document.getElementById("class-list");

  if (nameEl && usernameEl && classListEl) {
    const userID = localStorage.getItem("userID");
    const userName = localStorage.getItem("userName");

    if (!userID || userID === "null" || userID === "undefined") {
      window.location.href = "/";
      return;
    }

    nameEl.innerText = userName || "Loading...";
    usernameEl.innerText = "Student";

    fetch(`/user/${userID}/classes`)
      .then((res) => res.json())
      .then((data) => {
        if (data.success && data.classes && data.classes.length > 0) {
          data.classes.forEach((cls) => {
            const li = document.createElement("li");
            li.innerText = `${cls.title} (Grade: ${cls.grade})`;
            classListEl.appendChild(li);
          });
        } else {
          classListEl.innerHTML = "<li>No enrolled classes found.</li>";
        }
      })
      .catch((err) => {
        classListEl.innerHTML = "<li>Error loading classes.</li>";
        console.error(err);
      });
  }
});