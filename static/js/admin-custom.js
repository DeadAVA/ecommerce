document.addEventListener('DOMContentLoaded', function () {
    const editarButtons = document.querySelectorAll('.btn-editar');
    const formEditar = document.getElementById('formEditarCategoria');
    const inputNombre = document.getElementById('editarNombre');

    editarButtons.forEach(button => {
      button.addEventListener('click', () => {
        const id = button.getAttribute('data-id');
        const nombre = button.getAttribute('data-nombre');

        // Actualiza el valor del input en el modal
        inputNombre.value = nombre;

        // Establece la acción del formulario para apuntar al endpoint correcto
        formEditar.action = `/admin/categorias/editar/${id}`;
      });
    });
  });

  function cargarProducto(id, nombre, descripcion, precio, categoria_id, imagen_url) {
    document.getElementById('editarProductoForm').action = `/admin/productos/editar/${id}`;
    document.getElementById('editar-nombre').value = nombre;
    document.getElementById('editar-descripcion').value = descripcion;
    document.getElementById('editar-precio').value = precio;
    document.getElementById('editar-categoria').value = categoria_id;
    const imagenActual = document.getElementById('imagen-actual');
    imagenActual.innerHTML = imagen_url
      ? `<small>Imagen actual:</small><br><img src="${imagen_url}" width="60">`
      : '<small>No tiene imagen</small>';
  }


  document.querySelectorAll('.btn-edit-user').forEach(button => {
    button.addEventListener('click', () => {
        const id = button.getAttribute('data-id')
        const username = button.getAttribute('data-username')
        const nombre = button.getAttribute('data-nombre')
        const apellido = button.getAttribute('data-apellido')
        const email = button.getAttribute('data-email')
        const adminChecked = button.getAttribute('data-admin')

        document.getElementById('editar_id').value = id
        document.getElementById('username').value = username
        document.getElementById('nombre').value = nombre
        document.getElementById('apellido').value = apellido
        document.getElementById('email').value = email
        document.getElementById('admin').checked = adminChecked === 'checked'
        document.getElementById('password').value = ''  // Limpiar password
    })
})

  function abrirModal() {
    document.getElementById('editar_id').value = '';
    document.querySelectorAll('#direccionModal input, #direccionModal textarea').forEach(input => input.value = '');
  }

  function editarDireccion(id, usuario_id, direccion, colonia, ciudad, estado, cp, pais, telefono, referencias) {
    document.getElementById('editar_id').value = id;
    document.getElementById('usuario_id').value = usuario_id;
    document.getElementById('direccion').value = direccion;
    document.getElementById('colonia').value = colonia;
    document.getElementById('ciudad').value = ciudad;
    document.getElementById('estado').value = estado;
    document.getElementById('codigo_postal').value = cp;
    document.getElementById('pais').value = pais;
    document.getElementById('telefono').value = telefono;
    document.getElementById('referencias').value = referencias;
  }


document.addEventListener('DOMContentLoaded', function () {
  const dataDiv = document.getElementById('ventas-data');
  if (!dataDiv) return;

  const labels = JSON.parse(dataDiv.dataset.labels);
  const values = JSON.parse(dataDiv.dataset.values);

  const ctx = document.getElementById('ventasChart').getContext('2d');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Ventas Últimos 6 Meses',
        data: values,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
});
