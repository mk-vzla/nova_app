// Función para pedir confirmación antes de eliminar
function confirmarEliminacion(idJuego) {
    // Mostrar el cuadro de confirmación
    const confirmacion = confirm("¿Estás seguro de que deseas eliminar este juego? Esta acción no se puede deshacer.");
    
    // Si el usuario confirma, enviar el formulario
    if (confirmacion) {
        // Encontramos el formulario con el ID específico
        const formulario = document.getElementById(`form-eliminar-${idJuego}`);
        
        // Enviar el formulario
        formulario.submit();
    }
}