const API = 'http://127.0.0.1:8000';

const loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await response.json();

        if (response.ok && data.requires_verification) {
            localStorage.setItem('pending_email', email);
            alert(data.msg || 'Debes verificar tu cuenta primero.');
            window.location.href = 'verify.html';
        } else if (response.ok) {
            localStorage.setItem('access_token', data.access_token);
            alert('¡Bienvenido!');
            window.location.href = 'index.html';
        } else {
            alert('Error: ' + (data.detail || 'Credenciales inválidas'));
        }
    } catch (error) {
        console.error('Error en la conexión:', error);
        alert('Hubo un problema al conectar con el servidor.');
    }
});