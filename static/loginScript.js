document.getElementById('loginButton').addEventListener('click', SendLoginRequest);

document.getElementById("password").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        SendLoginRequest()
    }
});

function SendLoginRequest() {
  const username = document.getElementById("ID").value;
  const password = document.getElementById("password").value;


  fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username: username, password: password })
  })
  .then(response => response.json())
  .then(data => data_to_switch(data))

  
}

function data_to_switch(data) {
  console.log(data)

  if (data["success"]) {
    localStorage.setItem("name", data["User"]);
    localStorage.setItem("id", data["ID"]);
    window.location.href="/homepage"
  }
} 
