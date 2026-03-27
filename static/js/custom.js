(function() {
  'use strict';

  // Tiny Slider (sin cambios)
  var tinyslider = function() {
    var el = document.querySelectorAll('.testimonial-slider');

    if (el.length > 0) {
      var slider = tns({
        container: '.testimonial-slider',
        items: 1,
        axis: "horizontal",
        controlsContainer: "#testimonial-nav",
        swipeAngle: false,
        speed: 700,
        nav: true,
        controls: true,
        autoplay: true,
        autoplayHoverPause: true,
        autoplayTimeout: 3500,
        autoplayButtonOutput: false
      });
    }
  };
  tinyslider();

  // *** Eliminada función sitePlusMinus para evitar doble incremento ***

})();

// Esperar a DOMContentLoaded para manipular elementos y manejar modal
document.addEventListener('DOMContentLoaded', function () {
  const productModal = document.getElementById('productModal');
  if (productModal) {
    productModal.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      if (!button) return;

      const id = button.getAttribute('data-id');
      const nombre = button.getAttribute('data-nombre');
      const descripcion = button.getAttribute('data-descripcion');
      const precio = button.getAttribute('data-precio');
      const imagen = button.getAttribute('data-imagen');

      const titleElem = document.getElementById('modal-product-title');
      if (titleElem) titleElem.textContent = nombre || '';

      const descElem = document.getElementById('modal-product-description');
      if (descElem) descElem.textContent = descripcion || '';

      const priceElem = document.getElementById('modal-product-price');
      if (priceElem) priceElem.textContent = precio ? `$${precio}` : '';

      const imgElem = document.getElementById('modal-product-image');
      if (imgElem) imgElem.src = imagen || '';

      const form = document.getElementById('add-to-cart-form');
      if (form) {
        form.action = `/agregar/${id}` || '#';
      }
    });
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const rows = document.querySelectorAll('tbody tr');

  rows.forEach(row => {
    const increaseBtn = row.querySelector('.increase');
    const decreaseBtn = row.querySelector('.decrease');
    const qtyInput = row.querySelector('.quantity-amount');
    const priceCell = row.querySelector('.product-price');
    const totalCell = row.querySelector('.product-total');

    if (!increaseBtn || !decreaseBtn || !qtyInput || !priceCell || !totalCell) return;

    const itemId = increaseBtn.dataset.id;
    const unitPrice = parseFloat(priceCell.dataset.price);

    async function updateQuantityOnServer(newQty) {
      try {
        const response = await fetch('/cart/update_quantity', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            item_id: itemId,
            quantity: newQty
          }),
        });
        const data = await response.json();
        if (!data.success) {
          alert('Error actualizando cantidad: ' + data.message);
          return false;
        }
        return data;
      } catch (error) {
        alert('Error al conectar con el servidor');
        return false;
      }
    }

    async function updateTotal() {
      let qty = parseInt(qtyInput.value);
      if (isNaN(qty) || qty < 1) qty = 1;
      qtyInput.value = qty;

      const result = await updateQuantityOnServer(qty);
      if (result) {
        totalCell.textContent = '$' + result.total_item.toFixed(2);
        updateCartTotal();
      }
    }

    increaseBtn.addEventListener('click', async () => {
      let currentQty = parseInt(qtyInput.value);
      if (isNaN(currentQty)) currentQty = 0;
      const newQty = currentQty + 1;

      qtyInput.value = newQty;
      const result = await updateQuantityOnServer(newQty);
      if (result) {
        totalCell.textContent = '$' + result.total_item.toFixed(2);
        updateCartTotal();
      }
    });

    decreaseBtn.addEventListener('click', async () => {
      let currentQty = parseInt(qtyInput.value);
      if (isNaN(currentQty)) currentQty = 1;
      if (currentQty > 1) {
        const newQty = currentQty - 1;

        qtyInput.value = newQty;
        const result = await updateQuantityOnServer(newQty);
        if (result) {
          totalCell.textContent = '$' + result.total_item.toFixed(2);
          updateCartTotal();
        }
      }
    });

    qtyInput.addEventListener('change', updateTotal);
  });

  function updateCartTotal() {
    let totalGeneral = 0;
    document.querySelectorAll('tbody tr').forEach(row => {
      const totalCell = row.querySelector('.product-total');
      let totalText = totalCell ? totalCell.textContent.replace('$', '').trim() : '0';
      totalGeneral += parseFloat(totalText) || 0;
    });

    const totalGeneralElement = document.getElementById('total-general');
    if (totalGeneralElement) {
      totalGeneralElement.textContent = '$' + totalGeneral.toFixed(2);
    }

    const subtotalGeneralElement = document.getElementById('subtotal-general');
    if (subtotalGeneralElement) {
      subtotalGeneralElement.textContent = '$' + totalGeneral.toFixed(2);
    }
  }
});

// Esperar a DOMContentLoaded para manipular elementos
document.addEventListener('DOMContentLoaded', function () {
  const productModal = document.getElementById('productModal');
  if (productModal) {
    productModal.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      if (!button) return;

      // Obtén los datos desde los atributos del producto
      const id = button.getAttribute('data-id');
      const nombre = button.getAttribute('data-nombre');
      const descripcion = button.getAttribute('data-descripcion');
      const precio = button.getAttribute('data-precio');
      const imagen = button.getAttribute('data-imagen');

      // Asignar los datos al modal con chequeo si existen los elementos
      const titleElem = document.getElementById('modal-product-title');
      if (titleElem) titleElem.textContent = nombre || '';

      const descElem = document.getElementById('modal-product-description');
      if (descElem) descElem.textContent = descripcion || '';

      const priceElem = document.getElementById('modal-product-price');
      if (priceElem) priceElem.textContent = precio ? `$${precio}` : '';

      const imgElem = document.getElementById('modal-product-image');
      if (imgElem) imgElem.src = imagen || '';

      const form = document.getElementById('add-to-cart-form');
      if (form) {
        form.action = `/agregar/${id}` || '#';
      }
    });
  }
});


document.addEventListener('DOMContentLoaded', function () {
  const cpInput = document.querySelector('input[name="codigo_postal"]');
  const coloniaSelect = document.getElementById('colonia');

  if (cpInput && coloniaSelect) {
    cpInput.addEventListener('blur', function () {
      const input = cpInput.value.trim();
      
      if (input.length === 0) {
        coloniaSelect.innerHTML = '<option value="">Selecciona una colonia</option>';
        return;
      }
      
      if (input.length !== 5) {
        coloniaSelect.innerHTML = '<option value="">Ingresa un codigo valido (5 digitos)</option>';
        return;
      }

      // Buscar con el input (puede ser CP o ID de colonia)
      fetch(`/api/zones/colonias/${input}`)
        .then(res => {
          // Verificar si la respuesta es exitosa
          if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
          }
          return res.json();
        })
        .then(data => {
          coloniaSelect.innerHTML = '<option value="">Selecciona una colonia</option>';

          if (data.colonias && data.colonias.length > 0) {
            data.colonias.forEach(colonia => {
              const option = document.createElement('option');
              option.value = colonia.colonia;
              option.textContent = `${colonia.colonia} (${colonia.municipio})`;
              coloniaSelect.appendChild(option);
            });

            // Log del CP real si se busco por ID
            if (data.colonias[0].codigo_postal && data.colonias[0].codigo_postal !== input) {
              console.log(`Busqueda por ID ${input} -> CP real: ${data.colonias[0].codigo_postal}`);
            }
          } else {
            console.warn(`Entrada ${input} no tiene colonias registradas.`);
            alert(`El codigo ${input} no se encontro en nuestra base de datos. Por favor verifica que sea correcto.\n\nCodigos validos ejemplos: 01001 (CDMX), 28080 (Colima), 06600 (CDMX).`);
            coloniaSelect.innerHTML = '<option value="">Codigo no encontrado</option>';
          }
        })
        .catch(err => {
          console.error("Error al obtener colonias:", err);
          alert(`Error al cargar colonias: ${err.message}. Verifica tu conexion e intenta nuevamente.`);
          coloniaSelect.innerHTML = '<option value="">Error al cargar</option>';
        });
    });
  }
});

function toggleNuevaDireccion(select) {
  const form = document.getElementById("form-nueva-direccion");
  if (!form || !select) return;

  if (select.value === "nueva" || select.value === "") {
    form.style.display = "block";
  } else {
    form.style.display = "none";
  }
}

window.onload = function() {
  const direccionGuardada = document.getElementById("direccion_guardada");
  if (direccionGuardada) {
    toggleNuevaDireccion(direccionGuardada);
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const trackings = document.querySelectorAll(".tracking-info");

  trackings.forEach(el => {
    const trackingNumber = el.dataset.tracking;
    const envioId = el.dataset.envioId;

    fetch(`/api/rastreo/${trackingNumber}`)
      .then(response => response.json())
      .then(data => {
        if (data.status === "ok") {
          const eventos = data.data.events.map(e => `
            <li class="list-group-item">
              <strong>${e.location}</strong>: ${e.description} <br>
              <small class="text-muted">${e.datetime}</small>
            </li>
          `).join("");

          el.innerHTML = `
            <h5 class="text-success">${data.data.status}</h5>
            <ul class="list-group list-group-flush mt-2">${eventos}</ul>
          `;
        } else {
          el.innerHTML = `<div class="alert alert-warning">No se pudo obtener el estado del paquete.</div>`;
        }
      })
      .catch(() => {
        el.innerHTML = `<div class="alert alert-danger">Error de conexión al rastrear el paquete.</div>`;
      });
  });
});
