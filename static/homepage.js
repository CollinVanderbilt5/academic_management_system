document.addEventListener("DOMContentLoaded", () => {

  const username = localStorage.getItem("name");
  const user_id = localStorage.getItem("id");
  const data = localStorage.getItem("BackendData")

  console.log("localStorage contents:", localStorage);

  if (username) { 
    document.getElementById('name').innerText = "Hello " + username + "!";
  }
});
