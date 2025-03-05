document.addEventListener("DOMContentLoaded", function() {
    const clienteId = 1;  // Cambia esto al ID del cliente que deseas obtener
    const url = `http://127.0.0.1:8000/api/v1/clientes/${clienteId}`;

    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + sessionStorage.getItem('token'),  // Asegúrate de que el token esté almacenado en sessionStorage
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        // Aquí puedes actualizar el DOM con los datos del cliente
        document.getElementById('cliente-info').innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
});