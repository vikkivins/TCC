// profile.js

document.getElementById('profilePictureUpload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const errorElement = document.getElementById('uploadError');

    if (file) {
        const formData = new FormData();
        formData.append('profile_picture', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('profilePicture').style.backgroundImage = `url(${data.url})`;
                errorElement.style.display = "none";
            } else {
                showError(data.message);
            }
        })
        .catch(() => showError("Ocorreu um erro ao fazer o upload da imagem."));
    }
});

function showError(message) {
    const errorElement = document.getElementById('uploadError');
    errorElement.textContent = message;
    errorElement.style.display = "block";
}

document.addEventListener('DOMContentLoaded', function () {
    const successMessage = document.getElementById('uploadSuccess');
    if (successMessage) {
        setTimeout(function () {
            successMessage.style.display = 'none';
        }, 3000); // 3000 milissegundos = 3 segundos
    }
});
