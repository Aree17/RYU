document.addEventListener("DOMContentLoaded", function () {
    const showHidePass = document.getElementById('showHidePassword');
    const userPassword = document.getElementById('id_password');

    if (!showHidePass || !userPassword) return;

    showHidePass.addEventListener('click', function () {
        userPassword.type =
            userPassword.type === 'password' ? 'text' : 'password';
        this.classList.toggle('fa-eye-slash');
    });
})