document.addEventListener("DOMContentLoaded", () => {

  let username = localStorage.getItem("name");
  const user_id = localStorage.getItem("id");
  const account_type = localStorage.getItem("account")

  const advising_hold = document.getElementById("advising")
  
  let menu = document.getElementById('menu')
  menu.style.display = 'none'

  if (username == 'null') {
    menu.style.display = 'flex'
    document.getElementById('name_input').addEventListener("keydown", function(event) {
      if (event.key === "Enter") {
        menu.style.display = 'none'
        username = document.getElementById('name_input').value;
        localStorage.setItem("name", username);
      }
    })
  }

  switch (account_type)
    {
        case "Student":
            advising_hold.style.display = 'none'
        case "Professor":
            advising_hold.style.display = 'none'
    }

  console.log("localStorage contents:", localStorage);

  if (username) { 
    document.getElementById('name').innerText = "Hello " + username + "!";
  }
  if (account_type){
    document.getElementById('username').innerText = account_type
  }
});
