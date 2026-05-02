const loginForm = document.getElementById('loginForm'); // Asegúrate que tu <form> tenga este ID

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        // IMPORTANTE: Usamos '/auth/login' sin el localhost
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: email, // O 'email' según pida tu modelo
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Guardamos el token para otras peticiones
            localStorage.setItem('token', data.access_token);
            alert('¡Bienvenido!');
            // Redirigimos a la ruta que definimos en el main.py
            window.location.href = '/index';
        } else {
            alert('Error: ' + (data.detail || 'Credenciales inválidas'));
        }
    } catch (error) {
        console.error('Error en la conexión:', error);
        alert('Hubo un problema al conectar con el servidor.');
    }
});