(function () {
	'use strict'

	// Fetch all the forms we want to apply custom Bootstrap validation styles to
	var forms = document.querySelectorAll('.needs-validation')

	// Loop over them and prevent submission
	Array.prototype.slice.call(forms)
		.forEach(function (form) {
			form.addEventListener('submit', function (event) {
				if (!form.checkValidity()) {
					event.preventDefault()
					event.stopPropagation()
				}

				form.classList.add('was-validated')
			}, false)
		})
})()

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