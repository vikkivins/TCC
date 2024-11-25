const video = document.getElementById('video-background');

// Controle de reversão usando um intervalo dinâmico
function playReverse() {
    const frameDuration = 0.033; // Duração aproximada de cada quadro (30 fps)
    const updateRate = frameDuration * 1000; // Converte para milissegundos

    const reverseInterval = setInterval(() => {
        if (video.currentTime > 0) {
            video.currentTime = Math.max(0, video.currentTime - frameDuration); // Atualiza o tempo do vídeo
        } else {
            // Quando chegar ao início, limpa o intervalo e reinicia normalmente
            clearInterval(reverseInterval);
            video.pause();
            video.playbackRate = 1;
            video.play();
        }
    }, updateRate); // Define o intervalo de atualização
}

// Evento para iniciar a reversão ao término do vídeo
video.addEventListener('ended', () => {
    video.pause(); // Pausa no final
    playReverse(); // Inicia reversão
});

let currentStep = 1;

function showStep(step) {
    document.querySelectorAll(".step").forEach((element, index) => {
        element.style.display = index + 1 === step ? "block" : "none";
    });
}

function nextStep() {
    if (validateStep(currentStep)) {
        currentStep++;
        updateStepInForm(currentStep);
        document.getElementById("wizardForm").submit();
    }
}

function goBack() {
    const stepInput = document.querySelector('input[name="step"]');
    if (stepInput) {
        let currentStep = parseInt(stepInput.value, 10);
        if (currentStep > 1) {
            stepInput.value = currentStep - 1;
            // Ignora validações ao retroceder
            const form = document.getElementById("wizardForm");
            form.noValidate = true;
            form.submit();
        }
    }
}

function updateStepInForm(step) {
    document.querySelector("input[name='step']").value = step;
}

function validateStep(step) {
    if (step === 1) {
        const username = document.getElementById("username").value;
        if (!/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(username)) {
            alert("O nome de usuário é inválido.");
            return false;
        }
    } else if (step === 2) {
        const birthDate = document.getElementById("birth_date").value;
        const age = calculateAge(new Date(birthDate));
        if (age < 14) {
            alert("Você deve ter pelo menos 14 anos.");
            return false;
        }
    } else if (step === 3) {
        const email = document.getElementById("email").value;
        if (!/^[^@]+@[^@]+\.[^@]+$/.test(email)) {
            alert("O e-mail é inválido.");
            return false;
        }
    } else if (step === 4) {
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;
        if (password !== confirmPassword) {
            alert("As senhas não coincidem.");
            return false;
        }
    }
    return true;
}

function calculateAge(birthDate) {
    const today = new Date();
    const age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        return age - 1;
    }
    return age;
}

// Mostra o primeiro passo ao carregar
document.addEventListener("DOMContentLoaded", () => showStep(currentStep));
