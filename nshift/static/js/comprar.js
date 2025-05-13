// Este script maneja la funcionalidad de agregar productos al carrito 

// Función para mostrar el modal de mensajes de compra
function mostrarModalCompra(mensaje, titulo = "Información", reload = false) {
    $('#modalMensajeCompraLabel').text(titulo);
    $('#modalMensajeCompraBody').html(mensaje);
    // Si reload es true, recarga al cerrar el modal
    if (reload) {
        $('#modalMensajeCompraFooter').html('<button type="button" class="btn btn-primary" data-bs-dismiss="modal" id="btnCerrarModalCompra">OK</button>');
        $('#modalMensajeCompra').off('hidden.bs.modal').on('hidden.bs.modal', function () {
            location.reload();
        });
    } else {
        $('#modalMensajeCompraFooter').html('<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>');
        $('#modalMensajeCompra').off('hidden.bs.modal');
    }
    const modal = new bootstrap.Modal(document.getElementById('modalMensajeCompra'));
    modal.show();
}

$(document).ready(function () {
    const conectadoRolId = parseInt($('#conectado-rol-id').val()); // Obtener el rol del usuario desde un input oculto

    $('.btn-comprar').on('click', function (event) {
        event.preventDefault();

        // Validar si el usuario tiene rol 1 o 3
        if (conectadoRolId === 1 || conectadoRolId === 3) {
            mostrarModalCompra('No se puede comprar con cuenta administrador/desarrollador.', 'Acceso restringido');
            return;
        }

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
            success: function (data) {
                if (data.mensaje) {
                    mostrarModalCompra(data.mensaje, '¡Éxito!', true);
                }
            },
            error: function (xhr) {
                const response = xhr.responseJSON;
                if (response && response.error) {
                    mostrarModalCompra(response.error, 'Error');
                } else {
                    mostrarModalCompra('Ocurrió un error al agregar el juego al carrito.', 'Error');
                }
            }
        });
    });
});


// Este script maneja la funcionalidad de eliminar productos del carrito
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


// Este script maneja la funcionalidad de proceder al pago
$(document).ready(function () {
    $('.btn-proceder-pago').on('click', function (event) {
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
            success: function (data) {
                console.log('Respuesta del servidor:', data);
                if (data.mensaje) {
                    alert(data.mensaje);
                    location.reload();
                } else if (data.error) {
                    alert(`Error: ${data.error}`);
                }
            },
            error: function (xhr) {
                const response = xhr.responseJSON;
                if (response && response.error) {
                    alert(response.error); // Mostrar el mensaje de error específico del servidor
                } else {
                    alert('Ocurrió un error al procesar el pago.');
                }
            }
        });
    });
});


// Este script maneja la funcionalidad del botón "MINI GAME"
$(document).ready(function () {
    // Manejar el botón "MINI GAME"
    $('#btn-mini-game').on('click', function () {
        window.location.href = '/mini_juego/';
    });
});