const form = document.getElementById('formulario_modificar_perfil');

const nombre = document.getElementById('nombre');
const password1 = document.getElementById('password1');
const password2 = document.getElementById('password2');
const direccion = document.getElementById('direccion');

$(document).ready(function () {
    $('#formulario_modificar_perfil').on('submit', function (event) {
        event.preventDefault(); // Evita el envío por defecto

        let valid = true;

        // Validación de Nombre Completo
        const nombre = $('#nombre').val().trim();
        if (nombre === '') {
            $('#nombre-error').text('El nombre es obligatorio.');
            valid = false;
        } else if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(\s[A-Za-zÁÉÍÓÚáéíóúÑñ]+)+$/.test(nombre)) {
            $('#nombre-error').text('El nombre debe contener al menos un nombre y un apellido.');
            valid = false;
        } else {
            $('#nombre-error').text('');
        }

        // Validación de Contraseña
        const password1 = $('#password1').val().trim();
        const password2 = $('#password2').val().trim();
        if (password1 === '') {
            $('#password1-error').text('La contraseña es obligatoria.');
            valid = false;
        } else if (password1.length < 6 || password1.length > 18) {
            $('#password1-error').text('La contraseña debe tener entre 6 y 18 caracteres.');
            valid = false;
        } else if (!/^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])\S+$/.test(password1)) {
            $('#password1-error').text('La contraseña debe contener al menos una letra mayúscula, una minúscula y un número.');
            valid = false;
        } else {
            $('#password1-error').text('');
        }

        if (password2 === '') {
            $('#password2-error').text('Por favor confirma tu contraseña.');
            valid = false;
        } else if (password2 !== password1) {
            $('#password2-error').text('Las contraseñas no coinciden.');
            valid = false;
        } else {
            $('#password2-error').text('');
        }

       
        // Validación de Dirección de Despacho
        let direccion = $('#direccion').val().trim();
        if (direccion === '') {
            $('#direccion-error').text('');
            direccion = null; // Enviar null si la dirección no se llena
        } else {
            $('#direccion-error').text('');
        }


        // Si todo es válido, enviar los datos al servidor
        if (valid) {
            const datos = {
                nombre: nombre,
                password1: password1,
                password2: password2,
                direccion: direccion,
            };

            $.ajax({
                url: $(this).attr('action'),
                type: 'POST',
                headers: {
                    'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val(),
                },
                contentType: 'application/json',
                data: JSON.stringify(datos),
                success: function (response) {
                    alert(response.mensaje);
                    location.reload(); // Recarga la página al finalizar
                },
                error: function (xhr) {
                    alert(xhr.responseJSON.error || 'Ocurrió un error.');
                },
            });
        }
    });
});