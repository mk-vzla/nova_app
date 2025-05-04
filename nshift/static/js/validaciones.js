const form = document.getElementById('formulario_registro');

const nombre = document.getElementById('nombre');
const alias = document.getElementById('alias');
const email = document.getElementById('email');
const password1 = document.getElementById('password1');
const password2 = document.getElementById('password2');
const fecha = document.getElementById('fecha');
const descripcion = document.getElementById('direccion');
// const rol =  document.getElementById('rol');


document.addEventListener('DOMContentLoaded', function () {
    nombre.focus();
});

form.addEventListener('submit', function (event) {
    event.preventDefault(); // Evita el envío del formulario por defecto

    let valid = true;

    // Nombre completo -- Expresión regular un nombre y un apellido al menos: /^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(\s[A-Za-zÁÉÍÓÚáéíóúÑñ]+)+$/
    if (nombre.value.trim() === '') {
        document.getElementById('nombre-error').textContent = 'El nombre es obligatorio.';
        valid = false;
    } else if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(\s[A-Za-zÁÉÍÓÚáéíóúÑñ]+)+$/.test(nombre.value.trim())) {
        document.getElementById('nombre-error').textContent = 'El nombre debe contener al menos un nombre y un apellido.';
        valid = false;
    } else if (nombre.value.trim().length > 50) {
        document.getElementById('nombre-error').textContent = 'El nombre no debe exceder los 50 caracteres.';
        valid = false;
    } else {
        document.getElementById('nombre-error').textContent = '';
    }

    // Alias
    if (alias.value.trim() === '') {
        document.getElementById('alias-error').textContent = 'El alias es obligatorio.';
        valid = false;
    } else if (alias.value.trim().length < 3) {
        document.getElementById('alias-error').textContent = 'El alias debe tener al menos 3 caracteres.';
        valid = false;
    } else if (alias.value.trim().length > 15) {
        document.getElementById('alias-error').textContent = 'El alias no debe exceder los 15 caracteres.';
        valid = false;
    } else if (palabrasProhibidas.includes(alias.value.trim().toLowerCase())) {
        document.getElementById('alias-error').textContent = 'El alias contiene palabras prohibidas.';
        valid = false;
    } else {
        document.getElementById('alias-error').textContent = '';
    }

    // Email -- Expresión regular email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (email.value.trim() === '') {
        document.getElementById('email-error').textContent = 'El correo electrónico es obligatorio.';
        valid = false;
    } else if (
        !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim()) 
    ) {
        document.getElementById('email-error').textContent = 'El correo electrónico no es válido.';
        valid = false;
    } else {
        document.getElementById('email-error').textContent = '';
    }

    // Contraseña -- Expresión regular contraseña: /^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])\S+$/
    if (password1.value.trim() === '') {
        document.getElementById('password1-error').textContent = 'La contraseña es obligatoria.';
        valid = false;
    } else if (password1.value.trim().length < 6 || password1.value.trim().length > 18) {
        document.getElementById('password1-error').textContent = 'La contraseña debe tener entre 6 y 18 caracteres.';
        valid = false;
    } else if (!/^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])\S+$/.test(password1.value.trim())) {
        document.getElementById('password1-error').textContent = 'La contraseña debe contener al menos una letra mayúscula, una minúscula y un número.';
        valid = false;
    } else {
        document.getElementById('password1-error').textContent = '';
    }

    if (password2.value.trim() === '') {
        document.getElementById('password2-error').textContent = 'Por favor confirme contraseña.';
        valid = false;
    } else if (password2.value !== password1.value) {
        document.getElementById('password2-error').textContent = 'Las contraseñas no coinciden.';
        valid = false;
    } else {
        document.getElementById('password2-error').textContent = '';
    }

    // Fecha de nacimiento
    if (fecha.value.trim() === '') {
        document.getElementById('fecha-error').textContent = 'La fecha de nacimiento es obligatoria.';
        valid = false;
    } else if (new Date(fecha.value) > new Date(new Date().setFullYear(new Date().getFullYear() - 13))) {
        document.getElementById('fecha-error').textContent = 'Debes tener al menos 13 años.';
        valid = false;
    } else {
        document.getElementById('fecha-error').textContent = '';
    }

    //Rol
    /*
    if (rol.value.trim() === '') {
        document.getElementById('rol-error').textContent = 'El Rol es obligatorio.';
        valid = false;
    } else {
        document.getElementById('rol-error').textContent = '';
    }
    */

    // Términos
    if (!document.getElementById('terminos').checked) {
        document.querySelector('.error-message').textContent = 'Debes aceptar los términos y condiciones.';
        valid = false;
    } else {
        document.querySelector('.error-message').textContent = '';
    }

    // Si todos los campos son válidos, puedes enviar el formulario o realizar otra acción (con jquery)
    if (valid) {
        console.log('Formulario válido. Enviando datos...');
        const usuario = {
            nombre_completo: $('#nombre').val().trim(),
            alias: $('#alias').val().trim(),
            email: $('#email').val().trim(),
            password: $('#password1').val().trim(),
            fecha_nacimiento: $('#fecha').val().trim(),
            direccion: $('#direccion').val(),
            rol: 2 // $('#rol').val().trim()
        };
    
        $.ajax({
            url: 'core/registrar/',
            type: 'POST',
            data: JSON.stringify(usuario),
            contentType: 'application/json',
            success: function (response) {
            alert(response.mensaje);
            $('#formulario_registro')[0].reset(); // Reinicia el formulario
            window.location.href = 'login'; // Redirige a la página de iniciar sesión
            },
            error: function (xhr) {
            const res = xhr.responseJSON;
            alert(res?.error || 'Error al registrar el usuario.');
            }
        });
    }
});

const limpiarButton = document.getElementById('limpiar');
limpiarButton.addEventListener('click', function () {
    form.reset(); // Reinicia el formulario
    document.querySelectorAll('.text-danger').forEach(error => error.textContent = ''); // Limpia los mensajes de error
    document.querySelector('.error-message').textContent = ''; // Limpia el mensaje de términos
});


document.addEventListener('DOMContentLoaded', function () {
    nombre.focus();
    cargarAliasSugeridos();
});

function cargarAliasSugeridos() {
    fetch('/core/api/alias-sugeridos/')
        .then(response => response.json())
        .then(data => {
            const aliasSugerenciasDiv = document.getElementById('alias-sugerencias');
            aliasSugerenciasDiv.innerHTML = ''; // Limpia las sugerencias anteriores
            data.alias_sugeridos.forEach(alias => {
                const aliasButton = document.createElement('button');
                aliasButton.type = 'button';
                aliasButton.className = 'btn btn-outline-secondary btn-sm';
                aliasButton.textContent = alias;
                aliasButton.onclick = () => {
                    document.getElementById('alias').value = alias;
                };
                aliasSugerenciasDiv.appendChild(aliasButton);
            });
        })
        .catch(error => console.error('Error al cargar alias sugeridos:', error));
}



































// Array de palabras prohibidas
const palabrasProhibidas = [
    "admin",
    "root",
    "password",
    "123456",
    "sexo",
    "violencia",
    "droga",
    "asesino",
    "hacker",
    "pirata",
    "fraude",
    "racismo",
    "odio",
    "terror",
    "bomba",
    "crimen",
    "ilegal",
    "prohibido",
    "malware",
    "phishing",
    "spam",
    "virus",
    "troll",
    "insulto",
    "ofensivo",
    "abusivo",
    "estafa",
    "pornografía",
    "nazi",
    "homofobia",
    "xenofobia",
    "pedofilia",
    "violador",
    "asesinato",
    "suicidio",
    "armas",
    "corrupción",
    "chantaje",
    "extorsión",
    "hack",
    "crack",
    "falsificación",
    "engaño",
    "mentira",
    "ilegalidad",
    "contrabando",
    "terrorismo",
    "radical",
    "odio",
    "discriminación",
    "prostitución",
    "mafioso",
    "delincuente",
    "viola",
    "alias"
  ];
