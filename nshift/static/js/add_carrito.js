$(document).ready(function () {
    // Manejar el clic en el botón "Añadir al Carrito"
    $('.add-to-cart-btn').on('click', function (e) {
        e.preventDefault(); // Evitar el comportamiento predeterminado del enlace
        console.log('Botón clickeado');

        // Obtener el ID del juego desde el atributo data-id
        const juegoId = $(this).data('id');

        // Enviar una solicitud AJAX al servidor
        $.ajax({
            url: '/core/carrito/', // Asegúrate de que termine con '/'
            type: 'POST',
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            data: {
                juego_id: juegoId
            },
            success: function (response) {
                alert(response.message);
            },
            error: function (xhr) {
                alert(`Error: ${xhr.responseJSON.error}`);
            }
        });
    });
});