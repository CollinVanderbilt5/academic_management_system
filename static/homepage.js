document.addEventListener("DOMContentLoaded", () => {

  const username = localStorage.getItem("name");
  const user_id = localStorage.getItem("id");
  const account_type = localStorage.getItem("account")

  console.log("localStorage contents:", localStorage);

  if (username) { 
    document.getElementById('name').innerText = "Hello " + username + "!";
  }
  if (account_type){
    document.getElementById('username').innerText = account_type
  }
});
