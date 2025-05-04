function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).innerText;
    navigator.clipboard.writeText(text).then(() => {
        // alert('URL copiada al portapapeles: ' + text);
    }).catch(err => {
        console.error('Error al copiar: ', err);
    });
}