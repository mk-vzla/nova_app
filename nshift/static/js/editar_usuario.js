$(document).ready(function () {
    // Selecciona todos los botones de edición
    $('.btn-editar').on('click', function () {
        // Obtén los datos del usuario desde los atributos del botón
        const email = $(this).data('email');
        const nombre = $(this).data('nombre');
        const alias = $(this).data('alias');
        const fecha = $(this).data('fecha');
        const direccion = $(this).data('direccion');
        const rol = $(this).data('rol');

        // Rellena los campos del formulario en el modal
        $('#editar_email').val(email);
        $('#editar_nombre').val(nombre);
        $('#editar_alias').val(alias);
        $('#editar_fecha').val(fecha);
        $('#editar_direccion').val(direccion);
        $('#editar_rol').val(rol);
    });

    // Validación y envío del formulario de edición
    $('#form_editar_usuario').on('submit', function (event) {
        event.preventDefault(); // Evitar el envío por defecto

        const usuario = {
            email: $('#editar_email').val(),
            nombre_completo: $('#editar_nombre').val(),
            alias: $('#editar_alias').val(),
            fecha_nacimiento: $('#editar_fecha').val(),
            direccion: $('#editar_direccion').val(),
            rol: $('#editar_rol').val()
        };

        // Enviar los datos al servidor mediante AJAX
        $.ajax({
            url: '/core/editar/',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken() // Obtener el token CSRF
            },
            contentType: 'application/json',
            data: JSON.stringify(usuario),
            success: function (data) {
                if (data.mensaje) {
                    alert(data.mensaje);
                    location.reload(); // Recargar la página para reflejar los cambios
                } else if (data.error) {
                    alert(data.error);
                }
            },
            error: function (xhr) {
                console.error('Error:', xhr);
                alert('Ocurrió un error al guardar los cambios.');
            }
        });
    });

    // Eliminación de usuario
    $('.btn-eliminar').on('click', function () {
        const email = $(this).data('email'); // Obtener el email del usuario a eliminar

        // Mostrar confirmación
        const confirmacion = confirm(`¿Estás seguro de que deseas eliminar al usuario con correo: ${email}?`);
        if (confirmacion) {
            // Enviar solicitud AJAX para eliminar al usuario
            $.ajax({
                url: '/core/eliminar/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken() // Obtener el token CSRF
                },
                contentType: 'application/json',
                data: JSON.stringify({ email: email }),
                success: function (data) {
                    if (data.mensaje) {
                        alert(data.mensaje);
                        location.reload(); // Recargar la página para reflejar los cambios
                    } else if (data.error) {
                        alert(data.error);
                    }
                },
                error: function (xhr) {
                    console.error('Error:', xhr);
                    alert('Ocurrió un error al eliminar el usuario.');
                }
            });
        }
    });

    // Función para obtener el token CSRF
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
});



// Mostrar las compras del usuario
$('.btn-compras').on('click', function () {
    const email = $(this).data('email'); // Obtener el email del usuario

    // Hacer una solicitud AJAX para obtener las compras
    $.ajax({
        url: `/core/compras/${email}/`,
        type: 'GET',
        success: function (data) {
            const compras = data.compras;
            const tablaCompras = $('#tabla-compras');
            tablaCompras.empty(); // Limpiar la tabla

            if (compras.length > 0) {
                compras.forEach(compra => {
                    const fila = `
                        <tr>
                            <td>${compra.id_compra}</td>
                            <td>${compra.usuario}</td>
                            <td>${compra.juego}</td>
                            <td>${compra.cantidad}</td>
                            <td>${compra.precio_total}</td>
                            <td>${compra.fecha_compra}</td>
                        </tr>
                    `;
                    tablaCompras.append(fila);
                });
            } else {
                tablaCompras.append('<tr><td colspan="6" class="text-center">No hay compras registradas.</td></tr>');
            }
        },
        error: function (xhr) {
            console.error('Error:', xhr);
            alert('Ocurrió un error al obtener las compras.');
        }
    });
});