document.addEventListener('DOMContentLoaded', function() {
    const rolField = document.querySelector('select[name="rol"]');
    const dniField = document.querySelector('.field-dni').closest('.form-group');
    const nombreField = document.querySelector('.field-nombre').closest('.form-group');
    const apellidosField = document.querySelector('.field-apellidos').closest('.form-group');
    const nussField = document.querySelector('.field-nuss').closest('.form-group');
    const ibanField = document.querySelector('.field-iban').closest('.form-group');
    const salarioField = document.querySelector('.field-salario').closest('.form-group');
    const encargadoField = document.querySelector('.field-encargado').closest('.form-group');
    const telefonoField = document.querySelector('.field-telefono').closest('.form-group');
    const cineField = document.querySelector('.field-cine').closest('.form-group');

    function toggleFields() {
        const rol = rolField.value;
        if (rol === '2') { // Cliente
            dniField.style.display = 'none';
            nombreField.style.display = 'none';
            apellidosField.style.display = 'none';
            nussField.style.display = 'none';
            ibanField.style.display = 'none';
            salarioField.style.display = 'none';
            encargadoField.style.display = 'none';
            telefonoField.style.display = 'none';
            cineField.style.display = 'none';
        } else if (rol === '3') { // Empleado
            dniField.style.display = 'none';
            nombreField.style.display = 'none';
            apellidosField.style.display = 'none';
            nussField.style.display = 'none';
            ibanField.style.display = 'none';
            salarioField.style.display = 'none';
            encargadoField.style.display = 'none';
            telefonoField.style.display = 'none';
            cineField.style.display = 'none';
        } else if (rol === '4') { // Gerente
            dniField.style.display = 'none';
            nombreField.style.display = 'none';
            apellidosField.style.display = 'none';
            nussField.style.display = 'none';
            ibanField.style.display = 'none';
            salarioField.style.display = 'none';
            encargadoField.style.display = 'none';
            telefonoField.style.display = 'none';
            cineField.style.display = 'none';
        }
    }

    rolField.addEventListener('change', toggleFields);
    toggleFields(); // Initial call to set the correct fields
});