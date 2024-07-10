const correctPasswordHash = 'b64d75539245c3ef0221ca1c7b07ec531cb3a393b330cb67b29a72df76a2021e'; // Hashed password

function hashPassword(password) {
    // Simple hash function (e.g., SHA-256)
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    return crypto.subtle.digest('SHA-256', data).then(hash => {
        let hashArray = Array.from(new Uint8Array(hash));
        let hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        return hashHex;
    });
}

function checkPassword() {
    const password = document.getElementById('password').value;
    const error = document.getElementById('error');
    hashPassword(password).then(hash => {
        if (hash === correctPasswordHash) {
            sessionStorage.setItem('authenticated', 'true');
            showProtectedContent();
        } else {
            error.style.display = 'block';
        }
    });
}

function showProtectedContent() {
    if (sessionStorage.getItem('authenticated') === 'true') {
        document.getElementById('protected-content').style.display = 'block';
        document.querySelector('.login').style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    showProtectedContent();
});
