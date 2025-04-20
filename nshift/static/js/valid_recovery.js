const form = document.getElementById('formulario_recupera');
const email = document.getElementById('email');

form.addEventListener('submit', function (event) {
    event.preventDefault();

    let valid = true;

    if (email.value.trim() === '') {
        $('#email-error').text('El correo es obligatorio.');
        valid = false;
    } else {
        $('#email-error').text('');
    }

    if (valid) {
        const datos = {
            email: email.value.trim()
        };

        $.ajax({
            url: 'core/recuperar_contra/',  // O la ruta que uses para `enviar_correo_recuperacion`
            type: 'POST',
            data: JSON.stringify(datos),
            contentType: 'application/json',
            success: function (response) {
                alert(response.mensaje || 'Correo enviado.');
                window.location.href = 'login';
            },
            error: function (xhr) {
                const res = xhr.responseJSON;
                alert(res?.error || 'Error al enviar el correo.');
            }
        });
    }
});

