document.addEventListener("DOMContentLoaded", () => {
  // Fill user info from localStorage
  const nameElem = document.getElementById("name");
  const permElem = document.getElementById("username");
  const userName = localStorage.getItem("name") || "John Doe";
  const accountType = localStorage.getItem("account") || "Student";
  nameElem.textContent = userName;
  permElem.textContent = accountType;

  // Event listeners
  document.getElementById('add').addEventListener('click', add_user);
  document.getElementById('remove').addEventListener('click', remove_user);
  document.getElementById("password_confirm").addEventListener("input", check_password_match);
  document.getElementById("password").addEventListener("input", check_password_match);
});

function getSelectedAccount() {
  const studentCheck = document.getElementById('stu'); 
  const profCheck = document.getElementById('prof'); 
  const advisorCheck = document.getElementById('adv'); 

  if (studentCheck.checked && !profCheck.checked && !advisorCheck.checked) return 0;
  if (profCheck.checked && !studentCheck.checked && !advisorCheck.checked) return 1;
  if (advisorCheck.checked && !studentCheck.checked && !profCheck.checked) return 2;
  return -1; // Invalid selection
}

function getYourAccountType() {
  const account = localStorage.getItem("account");
  switch (account) {
    case "Student": return 0;
    case "Professor": return 1;
    case "Advisor": return 2;
    default: return -1;
  }
}

function add_user() {
  const username = document.getElementById("ID").value.trim();
  const password = document.getElementById("password").value.trim();
  const confirm = document.getElementById("password_confirm").value.trim();
  const add_account = getSelectedAccount();

  if (add_account === -1) {
    alert("Please select exactly one account type to add!");
    return;
  }

  if (password !== confirm) {
    alert("Passwords must match!");
    return;
  }

  const your_account_type = getYourAccountType();
  if (your_account_type === -1) {
    alert("Your account type is invalid.");
    return;
  }

  fetch("/adduser", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ account_type: your_account_type, add_type: add_account, add_id: username, add_pass: password })
  })
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));
}

function remove_user() {
  const username = document.getElementById("ID").value.trim();
  const add_account = getSelectedAccount();
  if (add_account === -1) {
    alert("Please select exactly one account type to remove!");
    return;
  }

  const your_account_type = getYourAccountType();
  if (your_account_type === -1) {
    alert("Your account type is invalid.");
    return;
  }

  fetch("/removeuser", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ account_type: your_account_type, add_type: add_account, add_id: username })
  })
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));
}

function check_password_match() {
  const password = document.getElementById("password").value;
  const confirm = document.getElementById("password_confirm").value;
  const warning = document.getElementById("warning");
  warning.textContent = (password && confirm && password !== confirm) ? "Passwords do not match!" : "";
}
