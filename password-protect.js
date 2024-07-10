const correctPassword = 'Safar1telecom'; // Set your password here

function checkPassword() {
    const password = document.getElementById('password').value;
    const error = document.getElementById('error');
    if (password === correctPassword) {
        localStorage.setItem('authenticated', 'true');
        showProtectedContent();
    } else {
        error.style.display = 'block';
    }
}

function showProtectedContent() {
    if (localStorage.getItem('authenticated') === 'true') {
        document.getElementById('protected-content').style.display = 'block';
        document.querySelector('.login').style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    showProtectedContent();
});