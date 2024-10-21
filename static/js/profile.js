// profile.js

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB in bytes

        document.getElementById('profilePictureUpload').addEventListener('change', function(event) {
            const file = event.target.files[0];
            const errorElement = document.getElementById('uploadError');
            
            if (file) {
                if (file.size > MAX_FILE_SIZE) {
                    errorElement.textContent = "O arquivo é muito grande. O tamanho máximo é 10MB.";
                    errorElement.style.display = "block";
                    this.value = ''; // Clear the file input
                    return;
                }

                if (!['image/jpeg', 'image/png'].includes(file.type)) {
                    errorElement.textContent = "Por favor, selecione apenas arquivos JPG ou PNG.";
                    errorElement.style.display = "block";
                    this.value = ''; // Clear the file input
                    return;
                }

                errorElement.style.display = "none";
                const formData = new FormData();
                formData.append('file', file);

                fetch('/upload', {
                    method: 'POST',
                    body: formData
                }).then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error('Erro no upload');
                }).then(data => {
                    if (data.success) {
                        document.getElementById('profilePicture').style.backgroundImage = `url(${data.url})`;
                    } else {
                        errorElement.textContent = data.message;
                        errorElement.style.display = "block";
                    }
                }).catch(error => {
                    errorElement.textContent = "Ocorreu um erro ao fazer o upload da imagem.";
                    errorElement.style.display = "block";
                });
            }
        });