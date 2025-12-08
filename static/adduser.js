document.getElementById('add').addEventListener('click', add_user);
document.getElementById('remove').addEventListener('click', remove_user);
document.getElementById("password_confirm").addEventListener("input", check_password_match)
document.getElementById("password").addEventListener("input", check_password_match)

function add_user()
{
    const account = localStorage.getItem("account");

    const username = document.getElementById("ID").value;
    const password = document.getElementById("password").value;
    const confirm = document.getElementById("password_confirm").value;

    const studentCheck = document.getElementById('stu'); 
    const profCheck = document.getElementById('prof'); 
    const advisorCheck = document.getElementById('adv'); 

    let add_account = 9

    if (studentCheck.checked) {
        if (profCheck.checked || advisorCheck.checked){
            console.log("Can't add multiple account!")
            return
        }
        add_account = 0
    }
    else if (profCheck.checked) {
        if (advisorCheck.checked || studentCheck.checked){
            console.log("Can't add multiple account!")
            return
        }
        add_account = 1
    }
    else if (advisorCheck.checked){
        if (studentCheck.checked || profCheck.checked){
            console.log("Can't add multiple account!")
            return
        }
        add_account = 2
    }
    else {
        console.log("Please pick an account to add!")
        return
    }

    if (password != confirm) {
        console.log("Passwords Must Mathc!")
        return
    }

    //Grabbing your account type value
    let your_account_type = 9
    switch (account)
    {
        case "Student":
            your_account_type = 0
            break;
        case "Professor":
            your_account_type = 1
            break;
        case "Adivsor":
            your_account_type = 2
            break;
    }

    fetch("http://127.0.0.1:5000/adduser", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    //Using an enum for account types, 0 = student, 1 = prof, 2 = advisor
    body: JSON.stringify({ account_type : your_account_type, add_type : add_account, add_id : username, add_pass : password})
  })
  .then(response => response.json())
  .then(data => response(data))
}

function remove_user()
{
    const username = document.getElementById("ID").value;
    const account = localStorage.getItem("account")

    const studentCheck = document.getElementById('stu'); 
    const profCheck = document.getElementById('prof'); 
    const advisorCheck = document.getElementById('adv'); 

    if (studentCheck.checked) {
        if (profCheck.checked || advisorCheck.checked){
            console.log("Can't add multiple account!")
            return
        }
        add_account = 0
    }
    else if (profCheck.checked) {
        if (advisorCheck.checked || studentCheck.checked){
            console.log("Can't add multiple account!")
            return
        }
        add_account = 1
    }
    else if (advisorCheck.checked){
        if (studentCheck.checked || profCheck.checked){
            console.log("Can't add multiple account!")
            return
        }
        add_account = 2
    }
    else
        return;

    //Grabbing your account type value
    let your_account_type = 9
    switch (account)
    {
        case "Student":
            your_account_type = 0
            break;
        case "Professor":
            your_account_type = 1
            break;
        case "Adivsor":
            your_account_type = 2
            break;
    }

    fetch("http://127.0.0.1:5000/removeuser", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    //Using an enum for account types, 0 = student, 1 = prof, 2 = advisor
    body: JSON.stringify({ account_type : your_account_type, add_type : add_account, add_id : username})
    })
    .then(response => response.json())
    .then(data => response(data))

}

function check_password_match()
{
    const password = document.getElementById("password").value;
    const confirm = document.getElementById("password_confirm").value;
    const warning = document.getElementById("warning")
    if (password != confirm && confirm != "")
        warning.innerText = "Passwords do not match!"
    else
        warning.innerText = ""

}

function response(data){
    console.log(data)
}


