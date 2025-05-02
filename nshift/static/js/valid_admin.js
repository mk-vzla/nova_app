document.addEventListener('DOMContentLoaded', () => {
    const formAdd = document.getElementById('formulario_añadir_producto');
    const formModify = document.getElementById('formulario_modificar_producto');

    // Función para limpiar formularios y mensajes de error
    function limpiarFormulario(form) {
        form.reset(); 
        form.querySelectorAll('.text-danger').forEach(error => error.textContent = '');
    }

    // Botón limpiar para el formulario de añadir productos
    document.querySelector('#formulario_añadir_producto button[type="reset"]').addEventListener('click', () => {
        limpiarFormulario(formAdd);
    });

    // Botón limpiar para el formulario de modificar productos
    document.querySelector('#formulario_modificar_producto button[type="reset"]').addEventListener('click', () => {
        limpiarFormulario(formModify);
    });

    // Validación para el formulario de añadir productos
    formAdd.addEventListener('submit', (event) => {
        event.preventDefault();
        let valid = true;

        const categoria = document.getElementById('categoria');
        const plataforma = document.getElementById('plataforma');
        const nombre = document.getElementById('nombre');
        const descripcion = document.getElementById('descripcion');
        const cantidad = document.getElementById('cantidad');
        const precio = document.getElementById('precio');
        const imagen = document.getElementById('imagen');

        // Validar categoría
        if (categoria.value.trim() === '') {
            document.getElementById('categoria_error').textContent = 'La categoría es obligatoria.';
            valid = false;
        } else {
            document.getElementById('categoria_error').textContent = '';
        }

        // Validar plataforma
        if (plataforma.value.trim() === '') {
            document.getElementById('plataforma_error').textContent = 'La plataforma es obligatoria.';
            valid = false;
        } else {
            document.getElementById('plataforma_error').textContent = '';
        }

        // Validar nombre
        if (nombre.value.trim() === '') {
            document.getElementById('nombre_error').textContent = 'El nombre es obligatorio.';
            valid = false;
        } else {
            document.getElementById('nombre_error').textContent = '';
        }

        // Validar descripción
        if (descripcion.value.trim() === '') {
            document.getElementById('descripcion_error').textContent = 'La descripción es obligatoria.';
            valid = false;
        } else {
            document.getElementById('descripcion_error').textContent = '';
        }

        // Validar cantidad
        if (cantidad.value.trim() === '' || cantidad.value <= 0) {
            document.getElementById('cantidad_error').textContent = 'La cantidad debe ser mayor a 0.';
            valid = false;
        } else {
            document.getElementById('cantidad_error').textContent = '';
        }

        // Validar precio
        if (precio.value.trim() === '' || precio.value < 0) {
            document.getElementById('precio_error').textContent = 'El precio debe ser no menor que 0';
            valid = false;
        } else {
            document.getElementById('precio_error').textContent = '';
        }

        if (valid) {
            console.log('Formulario válido. Enviando datos...');
            const producto = {
                categoria: $('#categoria').val().trim(),
                plataforma: $('#plataforma').val().trim(),
                nombre: $('#nombre').val().trim(),
                descripcion: $('#descripcion').val().trim(),
                cantidad: parseInt($('#cantidad').val()),
                precio: parseFloat($('#precio').val()),
                imagen: $('#imagen').val().trim()
            };

            $.ajax({
                url: 'core/agregar_producto/',
                type: 'POST',
                data: JSON.stringify(producto),
                contentType: 'application/json',
                success: function (response) {
                    alert(response.mensaje);
                },
                error: function (xhr) {
                    const res = xhr.responseJSON;
                    alert(res?.error || 'Error al agregar el producto.');
                }
            });
        }
    });


    // Detectar cambios en el ID del producto y autocompletar campos
    const productoId = document.getElementById('producto_id');
    const categoriaModificar = document.getElementById('categoria_modificar');
    const plataformaModificar = document.getElementById('plataforma_modificar'); // si está en el HTML
    const nombreModificar = document.getElementById('nombre_modificar');
    const descripcionModificar = document.getElementById('descripcion_modificar');
    const imagenModificar = document.getElementById('imagen_modificar');
    const cantidadModificar = document.getElementById('cantidad_modificar');
    const precioModificar = document.getElementById('precio_modificar');

    $('#producto_id').on('change', function () {
        const id = $(this).val().trim();

        if (id !== '') {
            $.ajax({
                url: `/core/obtener_producto/${id}/`,
                type: 'GET',
                success: function (data) {
                    $('#categoria_modificar').val(data.categoria);
                    if ($('#plataforma_modificar').length) {
                        $('#plataforma_modificar').val(data.plataforma);
                    }
                    $('#nombre_modificar').val(data.nombre);
                    $('#descripcion_modificar').val(data.descripcion);
                    $('#imagen_modificar').val(data.imagen);
                    $('#cantidad_modificar').val(data.cantidad);
                    $('#precio_modificar').val(data.precio);
                },
                error: function () {
                    alert('No se encontró el producto.');
                    $('#formulario_modificar_producto')[0].reset();
                }
            });
        }
    });





    // Validación para el formulario de modificar productos
    formModify.addEventListener('submit', (event) => {
        event.preventDefault();
        let valid = true;

        const productoId = document.getElementById('producto_id');
        const categoriaModificar = document.getElementById('categoria_modificar');
        const nombreModificar = document.getElementById('nombre_modificar');
        const descripcionModificar = document.getElementById('descripcion_modificar');
        const cantidadModificar = document.getElementById('cantidad_modificar');
        const precioModificar = document.getElementById('precio_modificar');

        // Validar ID del producto
        if (productoId.value.trim() === '') {
            document.getElementById('producto_id_error').textContent = 'El ID del producto es obligatorio.';
            valid = false;
        } else {
            document.getElementById('producto_id_error').textContent = '';
        }

        // Validar categoría
        if (categoriaModificar.value.trim() === '') {
            document.getElementById('categoria_modificar_error').textContent = 'La categoría es obligatoria.';
            valid = false;
        } else {
            document.getElementById('categoria_modificar_error').textContent = '';
        }

        // Validar nombre
        if (nombreModificar.value.trim() === '') {
            document.getElementById('nombre_modificar_error').textContent = 'El nombre es obligatorio.';
            valid = false;
        } else {
            document.getElementById('nombre_modificar_error').textContent = '';
        }

        // Validar descripción
        if (descripcionModificar.value.trim() === '') {
            document.getElementById('descripcion_modificar_error').textContent = 'La descripción es obligatoria.';
            valid = false;
        } else {
            document.getElementById('descripcion_modificar_error').textContent = '';
        }

        // Validar cantidad
        if (cantidadModificar.value.trim() === '' || cantidadModificar.value < 0) {
            document.getElementById('cantidad_modificar_error').textContent = 'La cantidad debe serc ero o positivo';
            valid = false;
        } else {
            document.getElementById('cantidad_modificar_error').textContent = '';
        }

        // Validar precio
        if (precioModificar.value.trim() === '' || precioModificar.value < 0) {
            document.getElementById('precio_modificar_error').textContent = 'El precio debe ser cero o positivo.';
            valid = false;
        } else {
            document.getElementById('precio_modificar_error').textContent = '';
        }

        if (valid) {
            console.log('Formulario válido. Enviando datos...');
            const producto = {
                producto_id: $('#producto_id').val().trim(),
                categoria: $('#categoria_modificar').val().trim(),
                plataforma: $('#plataforma_modificar').length ? $('#plataforma_modificar').val().trim() : '',
                nombre: $('#nombre_modificar').val().trim(),
                descripcion: $('#descripcion_modificar').val().trim(),
                imagen: $('#imagen_modificar').val().trim(),
                cantidad: parseInt($('#cantidad_modificar').val()),
                precio: parseFloat($('#precio_modificar').val())
            };

            $.ajax({
                url: '/core/modificar_producto/',
                type: 'POST',
                data: JSON.stringify(producto),
                contentType: 'application/json',
                success: function (response) {
                    if (response.mensaje) {
                        alert(response.mensaje);
                        formModify.reset();
                    } else if (response.error) {
                        alert('Error: ' + response.error);
                    }
                },
                error: function (xhr) {
                    const res = xhr.responseJSON;
                    alert(res?.error || 'Error al modificar el producto.');
                }
            });
        }
    });
});


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