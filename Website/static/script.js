document.getElementById('loginButton').addEventListener('click', SendLoginRequest);

document.getElementById("password").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        SendLoginRequest()
    }
});


function GetFromBackend() {
  fetch("http://127.0.0.1:5000/hello")
  .then(response => response.json())
  .then(data => {
    alert(data.message)
    document.getElementById("responseText").textContent = data.message;
  })
  .catch(error => console.error("Error: ", error));
}

function SendLoginRequest() {
   const username = document.getElementById("username").value;
   const password = document.getElementById("password").value;


  fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username: username, password: password })
  })
  .then(response => response.json())
  .then(data => console.log(data));
}

function toggleDisplay(elementId) {
      var element = document.getElementById(elementId);
      if (element.style.display === "none") {
        element.style.display = "block"; // Or appropriate display type
      } else {
        element.style.display = "none";
      }
    }