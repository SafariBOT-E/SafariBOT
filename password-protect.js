const correctPasswordHash = '8be270c2e030806ea253e5a9700c792c910214c551a238d51e947fd30a6fc47a0424ceaf56d08f7c56da1aea8d0d079c9c989bdb2aca73e080ae54fa4071f238'; // Hashed password

function hashPassword(password) {
    // Simple hash function (e.g., SHA-512)
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    return crypto.subtle.digest('SHA-512', data).then(hash => {
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
