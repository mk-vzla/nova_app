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
