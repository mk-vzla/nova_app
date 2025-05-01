const form = document.getElementById('formulario_login');
const alias = document.getElementById('alias');
const password = document.getElementById('password');

// Comenzar en el primer campo.
document.addEventListener('DOMContentLoaded', function () {
    alias.focus();
});

form.addEventListener('submit', function (event) {
    event.preventDefault(); // Evita el envío del formulario por defecto

    let valid = true;

    // Alias
    if (alias.value.trim() === '') {
        $('#alias-error').text('El alias es obligatorio.');
        valid = false;
    } else {
        $('#alias-error').text('');
    }

    // Contraseña
    if (password.value.trim() === '') {
        $('#password-error').text('La contraseña es obligatoria.');
        valid = false;
    } else if (password.value.trim().length < 6 || password.value.trim().length > 18) {
        $('#password-error').text('La contraseña debe tener entre 6 y 18 caracteres.');
        valid = false;
    } else {
        $('#password-error').text('');
    }

    // Usar jQuery para conectarse a la aplicación
    if (valid) {
        const datos = {
            alias: alias.value.trim(),
            password: password.value.trim(),
        };

        $.ajax({
            url: 'core/conectarse/',
            type: 'POST',
            data: JSON.stringify(datos),
            contentType: 'application/json',
            success: function (response) {
                //alert('Conexión exitosa: ' + response.mensaje);
                //$('#formulario_login')[0].reset(); // Reinicia el formulario
                window.location.href = '/'; // Redirige a la página principal
            },
            error: function (xhr) {
                const res = xhr.responseJSON;
                alert(res?.error || 'Error al iniciar sesión.');
            }
        });
    }
});

