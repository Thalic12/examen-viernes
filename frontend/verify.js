const API = window.location.origin;
let intervalo;

// --- VERIFICAR OTP ---
async function verificarOTP() {
    const email = localStorage.getItem("pending_email") || localStorage.getItem("email");
    const code = document.getElementById("codigo").value;
    const mensajeElement = document.getElementById("mensaje");

    if (!code || code.length < 6) {
        mostrarMensaje("Ingresa un código válido de 6 dígitos", "red");
        return;
    }

    try {
        const res = await fetch(`${API}/auth/verify`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, code }) // 'code' coincide con el esquema Verify en FastAPI
        });

        const data = await res.json();

        if (res.ok) {
            // Guardamos el token de 3 días proporcionado por el backend
            localStorage.setItem("access_token", data.access_token);
            localStorage.removeItem("pending_email");
            
            alert("¡Verificación exitosa! Bienvenido.");
            window.location.href = "index.html"; // Redirige al CRUD
        } else {
            mostrarMensaje(data.detail || "Código incorrecto", "red");
        }
    } catch (error) {
        mostrarMensaje("Error de conexión con el servidor", "red");
    }
}

// --- REENVIAR OTP ---
async function reenviarOTP() {
    const email = localStorage.getItem("pending_email") || localStorage.getItem("email");

    try {
         const res = await fetch(`${API}/auth/resend-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        if (res.ok) {
            mostrarMensaje("Nuevo código enviado al correo", "green");
            iniciarTimer(); 
        }
    } catch (error) {
        mostrarMensaje("No se pudo reenviar el código", "red");
    }
}

// --- FUNCIONES AUXILIARES ---

function mostrarMensaje(texto, color) {
    const mensajeElement = document.getElementById("mensaje");
    mensajeElement.innerText = texto;
    mensajeElement.style.color = color;
    mensajeElement.style.display = "block";
}

function iniciarTimer() {
    let tiempo = 300; // 5 minutos exactos como en el backend
    if (intervalo) clearInterval(intervalo);

    intervalo = setInterval(() => {
        let min = Math.floor(tiempo / 60);
        let sec = tiempo % 60;

        document.getElementById("timer").innerText = 
            `${min}:${sec < 10 ? "0" : ""}${sec}`;

        if (tiempo <= 0) {
            clearInterval(intervalo);
            mostrarMensaje("El código ha expirado. Solicita uno nuevo.", "red");
        }
        tiempo--;
    }, 1000);
}

// Inicialización
document.addEventListener("DOMContentLoaded", () => {
    iniciarTimer();
    const emailActual = localStorage.getItem("pending_email") || localStorage.getItem("email");
    if (!emailActual) {
        window.location.href = "registro.html";
    }
});