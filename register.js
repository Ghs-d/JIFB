document.getElementById("registerForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const errorMessage = document.getElementById("errorMessage");
    const successMessage = document.getElementById("successMessage");

    errorMessage.style.display = "none";
    successMessage.style.display = "none";

    try {
        const response = await fetch("", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, email })
        });

        const data = await response.json();

        if (data.email_exists || data.username_exists) {
            let message = "Erro: ";
            if (data.email_exists) message += "Este email já está em uso. ";
            if (data.username_exists) message += "Este nome de usuário já está em uso.";
            errorMessage.textContent = message;
            errorMessage.style.display = "block";
        } else {
           
            // await fetch("", { ... });

            successMessage.textContent = "Registro disponível! Pronto para enviar.";
            successMessage.style.display = "block";
        }

    } catch (error) {
        errorMessage.textContent = "Erro ao verificar usuário. Tente novamente mais tarde.";
        errorMessage.style.display = "block";
    }
});