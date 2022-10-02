function PasswordVisibility() {
    var x = document.getElementById("password_mysql");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}