// static/js/like.js
$(document).ready(function () {
    console.log("Document ready");

    var csrf_token = $('meta[name=csrf-token]').attr('content');
    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    });

    $(".like-product").click(function () {
        const productId = $(this).data("id");
        const likeButton = $(this);
        const likeCount = likeButton.next(".like-count");

        console.log("Liking product with ID:", productId);

        $.ajax({
            url: "/like",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ product_id: productId }),
            success: function (response) {
                console.log("AJAX success");
                alert(response.message);
                likeCount.text(response.likes);
                console.log("Success:", response.message);
            },
            error: function (xhr, status, error) {
                console.log("AJAX error");
                let errorMessage = "An error occurred";
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                alert(errorMessage);
                console.log("Error:", errorMessage);
            }
        });
    });
});