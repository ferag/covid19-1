var submitted = false;
var errorMessage = "No has aceptado los términos y condiciones"

function isChecked() {
  document.getElementById("terms").checked; 
}
function checkTerms() {
  document.getElementById('error').innerHTML = !document.getElementById("terms").checked && this.submitted ? this.errorMessage : "";
}
function onLogin() {
  if (document.getElementById("terms").checked) {
    document.location.href = "/start"
  }
  else {
    document.getElementById('error').innerHTML = this.errorMessage
  }
  this.submitted = true;
}
