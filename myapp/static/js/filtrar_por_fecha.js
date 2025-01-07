document.addEventListener('DOMContentLoaded', () => {
    const desdeInput = document.getElementById('date_filterp_desde');
    const hastaInput = document.getElementById('date_filterp_hasta');

    const fetchAndUpdateTable = () => {
        const desde = desdeInput.value;
        const hasta = hastaInput.value;

        fetch(`{% url 'listar_control_unidades' %}?date_filterp_desde=${desde}&date_filterp_hasta=${hasta}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud: ' + response.statusText);
                }
                return response.text();
            })
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newTable = doc.querySelector('.container').innerHTML;
                document.querySelector('.container').innerHTML = newTable;
            })
            .catch(error => console.error('Error al actualizar los datos:', error));
    };

    [desdeInput, hastaInput].forEach(input => {
        input.addEventListener('change', fetchAndUpdateTable);
    });
});
