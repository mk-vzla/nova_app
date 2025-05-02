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


document.addEventListener('DOMContentLoaded', function () {
    const btnBuscar = document.getElementById('btnEjecutarBusqueda');
    const resultadosDiv = document.getElementById('resultadosBusqueda');
    const formBuscarJuego = document.getElementById('formBuscarJuego');
    const modalBuscarJuego = document.getElementById('modalBuscarJuego');

    // Prevenir el cierre del modal al presionar Enter
    formBuscarJuego.addEventListener('submit', (event) => {
        event.preventDefault(); // Evita el comportamiento predeterminado del formulario
        ejecutarBusqueda(); // Llama a la función de búsqueda al presionar Enter
    });

    // Evitar que el modal se cierre al presionar Enter en cualquier campo
    modalBuscarJuego.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Evita que el Enter cierre el modal
            ejecutarBusqueda(); // Llama a la función de búsqueda al presionar Enter
        }
    });

    // Manejar la búsqueda al hacer clic en el botón
    btnBuscar.addEventListener('click', ejecutarBusqueda);

    // Función para ejecutar la búsqueda
    function ejecutarBusqueda() {
        const nombreJuego = document.getElementById('nombreJuego').value.trim();
        if (!nombreJuego) {
            resultadosDiv.innerHTML = '<p class="text-warning">Escribe un nombre de juego.</p>';
            return;
        }
        resultadosDiv.innerHTML = '<p class="text-info">Buscando...</p>';

        fetch(`${buscarUrl}?query=${encodeURIComponent(nombreJuego)}`)
            .then(resp => resp.json())
            .then(data => {
                resultadosDiv.innerHTML = '';
                if (data.error) {
                    resultadosDiv.innerHTML = `<p class="text-danger">${data.error}</p>`;
                } else if (data.resultados.length === 0) {
                    resultadosDiv.innerHTML = '<p class="text-warning">No se encontraron resultados.</p>';
                } else {
                    data.resultados.forEach(juego => {
                        resultadosDiv.innerHTML += `
                            <div class="card mb-3">
                                <div class="row g-0">
                                    <div class="col-md-4">
                                        <img src="${juego.image}" class="img-fluid rounded-start" alt="${juego.aliases}">
                                    </div>
                                    <div class="col-md-8">
                                        <div class="card-body">
                                            <dl class="row mb-0">
                                                <dt class="col-sm-4 text-dark">Alias:</dt>
                                                <dd class="col-sm-8 text-dark">${juego.aliases}</dd>

                                                <dt class="col-sm-4 text-dark">Descripción:</dt>
                                                <dd class="col-sm-8 text-dark">${juego.deck}</dd>

                                                <dt class="col-sm-4 text-dark">Lanzamiento:</dt>
                                                <dd class="col-sm-8 text-dark">${juego.original_release_date}</dd>

                                                <dt class="col-sm-4 text-dark">Plataformas:</dt>
                                                <dd class="col-sm-8 text-dark">${juego.platforms.join(', ')}</dd>

                                                <dt class="col-sm-4 text-dark">Ratings/Edades:</dt>
                                                <dd class="col-sm-8 text-dark">${juego.original_game_rating.join(', ')}</dd>
                                            </dl>
                                        </div>
                                    </div>
                                </div>
                            </div>`;
                    });
                }
            })
            .catch(err => {
                console.error('Error al realizar la búsqueda:', err);
                resultadosDiv.innerHTML = '<p class="text-danger">Error al realizar la búsqueda.</p>';
            });
    }
});