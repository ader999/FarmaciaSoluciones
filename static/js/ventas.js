$(document).ready(function() {
    var dollarRate = 0;

    // Inicialmente, desactivar el botón de vender
    $('#vender').prop('disabled', true);


    // Obtener la tasa de cambio del dólar al cargar la página
    $.ajax({
        url: '/get_dollar_rate',
        method: 'GET',
        success: function(response) {
            dollarRate = response.dollar_rate;
        }
    });

    // Función para actualizar el subtotal de un producto
    function updateSubtotal(row) {
        var price = parseFloat(row.find('td:nth-child(2)').text());
        var quantity = parseInt(row.find('input[name="cantidad"]').val());
        var subtotal = price * quantity;
        row.find('td:nth-child(4)').text(subtotal.toFixed(2));
        updateTotal();
    }

    // Función para actualizar el total de la factura
    function updateTotal() {
        var total = 0;
        $('#selectedProducts tbody tr').each(function() {
            var subtotal = parseFloat($(this).find('td:nth-child(4)').text());
            total += subtotal;
        });
        $('#total').text(total.toFixed(2));
        var totalInDollars = total / dollarRate;
        $('#total_dollars').text(totalInDollars.toFixed(2));

    }

    // Manejar la búsqueda de productos
    $('#searchTerm').on('input', function() {
        var term = $(this).val().trim();
        if (term === "") {
            $('#searchResults tbody').empty();
            return; // No hacer la solicitud AJAX si el término de búsqueda está vacío
        }

        $.ajax({
            url: '/buscar',
            method: 'POST',
            data: { term: term },
            success: function(response) {
                var resultsTable = $('#searchResults tbody');
                resultsTable.empty();
                response.forEach(function(product) {
                    resultsTable.append('<tr class="search-result" data-id="' + product[0] + '" data-name="' + product[1] + '" data-price="' + product[2] + '"><td>' + product[1] + '</td><td>' + product[2] + '</td></tr>');
                });

                // Manejar clics en los resultados de búsqueda
                $('.search-result').off('click').on('click', function() {
                    var id = $(this).data('id');
                    var name = $(this).data('name');
                    var price = $(this).data('price');
                    var selectedTable = $('#selectedProducts tbody');

                    // Verificar si el producto ya está en la tabla de seleccionados
                    var exists = false;
                    selectedTable.find('tr').each(function() {
                        if ($(this).data('id') == id) {
                            exists = true;
                        }
                    });

                    if (!exists) {
                        var newRow = $('<tr data-id="' + id + '"><td>' + name + '</td><td>' + price + '</td><td><input type="number" name="cantidad" value="1" min="1"></td><td></td></tr>');
                        selectedTable.append(newRow);
                        updateSubtotal(newRow);

                        // Manejar cambios en la cantidad
                        newRow.find('input[name="cantidad"]').on('input', function() {
                            updateSubtotal(newRow);
                        });
                    }
                });
            }
        });
    });

    // Manejar el clic en el botón para limpiar la tabla de productos seleccionados
    $('#clearTable').on('click', function() {
        $('#selectedProducts tbody').empty();
        $('#searchResults tbody').empty();
        $('#paymentAmount').val('');
        $('#searchTerm').val('');
        updateTotal(); // Actualizar el total a 0
        $('#vender').prop('disabled', true);
    });

    // Manejar el clic en el botón de vender
    $('#vender').on('click', function() {
    var totalCordobas = parseFloat($('#total').text());
    var totalDolares = parseFloat($('#total_dollars').text());
    var paymentAmount = parseFloat($('#paymentAmount').val());
    var vuelto = paymentAmount - totalCordobas;

    if (isNaN(paymentAmount)) {
        alert('Se requiere la cantidad con la que se está pagando.');
        return;
    }
    if (paymentAmount < totalCordobas) {
        alert('La cantidad pagada no es suficiente.');
        return;
    }

    var productos = [];
    $('#selectedProducts tbody tr').each(function() {
        var nombre = $(this).find('td:nth-child(1)').text();
        var precio = $(this).find('td:nth-child(2)').text();
        var cantidad = $(this).find('input[name="cantidad"]').val();
        var subtotal = $(this).find('td:nth-child(4)').text();
        productos.push({
            nombre: nombre,
            precio: parseFloat(precio),
            cantidad: parseInt(cantidad),
            subtotal: parseFloat(subtotal)
        });
    });

    // Enviar datos al servidor para confirmar la venta
    fetch('/confirmar_venta', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            totalCordobas: totalCordobas,
            totalDolares: totalDolares,
            productos: productos
        })
    }).then(response => response.json()).then(data => {
        if (data.success) {
            var ventaDetallesTable = $('#ventaDetalles tbody');
            ventaDetallesTable.empty();
            productos.forEach(function(producto) {
                ventaDetallesTable.append('<tr><td>' + producto.nombre + '</td><td>' + producto.precio.toFixed(2) + '</td><td>' + producto.cantidad + '</td><td>' + producto.subtotal.toFixed(2) + '</td></tr>');
            });

            $('#modalTotalCordobas').text(totalCordobas.toFixed(2));
            $('#modalTotalDolares').text(totalDolares.toFixed(2));
            $('#vuelto').text(vuelto.toFixed(2));

            // Mostrar la modal
            $('#ventaModal').modal('show');

            // Registrar la venta en un archivo de texto
            var parametros = [
                productos.map(p => `${p.nombre} ${p.precio} ${p.cantidad} ${p.subtotal}`).join('\n'),
                totalCordobas.toFixed(2),
                paymentAmount.toFixed(2),
                vuelto.toFixed(2)
            ];

            fetch('/registrar_venta', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    usuario: 'Nombre del Usuario', // Aquí puedes agregar el nombre del usuario dinámicamente
                    parametros: parametros
                })
            }).then(response => response.json()).then(data => {
                if (data.success) {
                    console.log('Venta registrada correctamente.');
                }
            });
        }
    });
});



    // Manejar el evento de ocultar la modal (cerrar)
    $('#ventaModal').on('hide.bs.modal', function() {
        // Limpiar los datos de la venta al cerrar la modal
        $('#selectedProducts tbody').empty();
        $('#searchResults tbody').empty();
        $('#total').text('0.00');
        $('#total_dollars').text('0.00');
        $('#paymentAmount').val('');
        $('#searchTerm').val('');
        $('#vender').prop('disabled', true);
    });

     $('#paymentAmount').on('input', function() {
         $('#vender').prop('disabled', false);

     });


    // Manejar el clic en el botón de imprimir dentro de la modal
    $('#printVenta').on('click', function() {
        // Recolectar los datos que se mostrarán en la vista de impresión
        var totalCordobas = $('#modalTotalCordobas').text();
        var totalDolares = $('#modalTotalDolares').text();
        var vuelto = $('#vuelto').text();
        var productos = [];

        // Recolectar los detalles de cada producto vendido
        $('#ventaDetalles tbody tr').each(function() {
            var nombre = $(this).find('td:nth-child(1)').text();
            var precio = $(this).find('td:nth-child(2)').text();
            var cantidad = $(this).find('td:nth-child(3)').text();
            var subtotal = $(this).find('td:nth-child(4)').text();
            productos.push({
                nombre: nombre,
                precio: precio,
                cantidad: cantidad,
                subtotal: subtotal
            });
        });

        // Enviar los datos al servidor para procesar la impresión
        fetch('/imprimir_venta', {
            method: 'POST', // Puedes usar GET si prefieres
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                totalCordobas: totalCordobas,
                totalDolares: totalDolares,
                vuelto: vuelto,
                productos: productos
            })
        }).then(response => response.json())
          .then(data => {
              // Aquí puedes manejar cualquier respuesta del servidor si es necesario
              console.log('Datos enviados para impresión:', data);
          })
          .catch(error => {
              console.error('Error al enviar datos para impresión:', error);
          });
    });






});



