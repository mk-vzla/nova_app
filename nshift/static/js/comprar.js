$(document).ready(function() {
    console.log('Script cargado correctamente'); // Depuración

    const $botonesComprar = $('.btn-comprar');
    console.log('Botones encontrados:', $botonesComprar.length); // Depuración

    $botonesComprar.on('click', function(event) {
        event.preventDefault();
        console.log('Botón clickeado'); // Depuración

        const productoId = $(this).data('producto-id');
        console.log('Producto ID:', productoId); // Depuración

        const csrfToken = $('[name=csrfmiddlewaretoken]').val();
        console.log('CSRF Token:', csrfToken); // Depuración

        $.ajax({
            url: '/core/agregar_al_carrito/',
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
                } else if (data.error) {
                    alert(`Error: ${data.error}`);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                if (xhr.status === 401) {
                    alert('Usuario no conectado. Por favor, inicia sesión para añadir productos al carrito.');
                } else {
                    alert('Ocurrió un error al agregar el producto al carrito.');
                }
            }
        });
    });
});