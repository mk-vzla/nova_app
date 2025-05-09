$(document).ready(function() {
    const $botonesComprar = $('.btn-comprar');

    $botonesComprar.on('click', function(event) {
        event.preventDefault();

        const productoId = $(this).data('producto-id');
        const csrfToken = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/core/agregar_al_carrito/',
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            contentType: 'application/json',
            data: JSON.stringify({ producto_id: productoId }),
            success: function(data) {
                if (data.mensaje) {
                    alert(data.mensaje);
                    location.reload(); // Recargar la página para reflejar los cambios
                }
            },
            error: function(xhr) {
                const response = xhr.responseJSON;
                if (response && response.error) {
                    alert(response.error); // Mostrar el mensaje de error
                } else {
                    alert('Ocurrió un error al agregar el juego al carrito.');
                }
            }
        });
    });
});



$(document).ready(function() {
    console.log('Script cargado correctamente'); // Depuración

    const $botonesEliminar = $('.btn-eliminar');
    console.log('Botones de eliminar encontrados:', $botonesEliminar.length); // Depuración

    $botonesEliminar.on('click', function(event) {
        event.preventDefault();
        console.log('Botón de eliminar clickeado'); // Depuración

        const productoId = $(this).data('producto-id');
        console.log('Producto ID a eliminar:', productoId); // Depuración

        const csrfToken = $('[name=csrfmiddlewaretoken]').val();
        console.log('CSRF Token:', csrfToken); // Depuración

        $.ajax({
            url: '/core/eliminar_del_carrito/',
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            contentType: 'application/json',
            data: JSON.stringify({ producto_id: productoId }),
            success: function(data) {
                console.log('Respuesta del servidor:', data); // Depuración
                if (data.mensaje) {
                    alert(data.mensaje);
                    location.reload(); // Recargar la página para actualizar el carrito
                } else if (data.error) {
                    alert(`Error: ${data.error}`);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                if (xhr.status === 401) {
                    alert('Usuario no conectado. Por favor, inicia sesión para eliminar productos del carrito.');
                } else {
                    alert('Ocurrió un error al eliminar el producto del carrito.');
                }
            }
        });
    });
});



$(document).ready(function() {
    $('.btn-proceder-pago').on('click', function(event) {
        event.preventDefault();

        const confirmacion = confirm('¿Se realizó el pago?');
        if (!confirmacion) {
            alert('Pago no realizado.');
            return;
        }

        const csrfToken = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/core/proceder_al_pago/',
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(data) {
                console.log('Respuesta del servidor:', data);
                if (data.mensaje) {
                    alert(data.mensaje);
                    location.reload();
                } else if (data.error) {
                    alert(`Error: ${data.error}`);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Ocurrió un error al procesar el pago.');
            }
        });
    });
});