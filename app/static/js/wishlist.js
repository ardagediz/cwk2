// static/js/wishlist.js
$(document).ready(function () {
    $(".add-to-wishlist").click(function () {
        const productId = $(this).data("id");
        const productName = $(this).data("name");
        const productDescription = $(this).data("description");
        const productPrice = $(this).data("price");

        // Create a form dynamically
        const form = $('<form>', {
            'method': 'POST',
            'action': '/wishlist/add'
        });

        // Add hidden fields to the form
        form.append($('<input>', {
            'type': 'hidden',
            'name': 'product_id',
            'value': productId
        }));
        form.append($('<input>', {
            'type': 'hidden',
            'name': 'product_name',
            'value': productName
        }));
        form.append($('<input>', {
            'type': 'hidden',
            'name': 'product_description',
            'value': productDescription
        }));
        form.append($('<input>', {
            'type': 'hidden',
            'name': 'product_price',
            'value': productPrice
        }));

        // Append the form to the body and submit it
        $('body').append(form);
        form.submit();
    });
});