const LOGIN_URL = "/auth/login";
const TOKEN_KEY = "access_token";

document.addEventListener("DOMContentLoaded", () => {
    setupLoginPage();
});

function setupLoginPage() {
    // 1. Verificación de sesión existente
    const token = localStorage.getItem(TOKEN_KEY);
    
    // Solo redirecciona si hay un token válido y NO es un string "null"/"undefined"
    if (token && token !== "undefined" && token !== "null") {
        console.log("Token detectado, redirigiendo a index...");
        window.location.href = "/index"; 
        return;
    }

    const loginForm = document.getElementById("login-form");
    const loginError = document.getElementById("login-error");
    const emailInput = document.getElementById("login-email");
    
    // Autocompletar email desde URL si existe
    const params = new URLSearchParams(window.location.search);
    const email = params.get("email");
    if (emailInput && email) {
        emailInput.value = email;
    }

    if (!loginForm) return;

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        if (loginError) {
            loginError.style.display = "none";
            loginError.textContent = "";
        }

        const loginEmail = document.getElementById("login-email").value;
        const password = document.getElementById("login-password").value;

        try {
            const res = await fetch(LOGIN_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: loginEmail, password }),
            });

            const data = await res.json().catch(() => ({}));

            if (!res.ok) {
                if (loginError) {
                    loginError.textContent = data?.detail || "Correo o contraseña inválidos";
                    loginError.style.display = "block";
                }
                return;
            }

            // 2. Guardar token y redirigir a /index
            if (data.access_token) {
                localStorage.setItem(TOKEN_KEY, data.access_token);
                window.location.href = "/index"; 
            } else {
                throw new Error("No se recibió el token de acceso");
            }

        } catch (error) {
            console.error("Error en login:", error);
            if (loginError) {
                loginError.textContent = "Error de conexión con el servidor";
                loginError.style.display = "block";
            }
        }
    });
}
