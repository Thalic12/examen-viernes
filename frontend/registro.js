const API = "http://127.0.0.1:8000";

document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const mensajeElement = document.getElementById("mensaje");
    const name = document.getElementById("reg-name").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;

    // Limpiar mensajes previos
    mensajeElement.style.display = "none";
    mensajeElement.innerText = "";

    try {
        const res = await fetch(`${API}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });

        const data = await res.json();

        if (res.ok) {
            // 1. Guardamos el email en el localStorage para que verify.js sepa a quién validar
            localStorage.setItem("pending_email", email);
            
            alert("¡Registro exitoso! Revisa tu correo para el código de verificación.");
            
            // 2. Redirigimos a la pantalla de OTP que ya tienes configurada
            window.location.href = "verify.html";
        } else {
            // Mostrar error del backend (ej: "El correo ya está registrado")
            mensajeElement.innerText = data.detail || "Error en el registro";
            mensajeElement.style.display = "block";
            mensajeElement.style.color = "red";
        }
    } catch (error) {
        mensajeElement.innerText = "No se pudo conectar con el servidor";
        mensajeElement.style.display = "block";
    }
});