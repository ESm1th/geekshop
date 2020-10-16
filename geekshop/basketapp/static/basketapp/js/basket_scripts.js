window.onload = function () {
    $('.basket_item').on('change', 'input[type="number"]', function (event) {

        var init_object = event.target;
        var closest_div = init_object.closest('div');

        $.ajax ({

            url: init_object.getAttribute('url'),
            data: {'quantity': init_object.value},
            success: function(data) {
                if (data.deleted) {
                    $(closest_div).remove();
                    $('.card-pic').children('p').html(data.total_items_quantity);
                } else {
                    $(closest_div).children('p').children('span').html(data.price);
                };
                $('.price').children('span').html(data.total_price);
            },
        });

        event.preventDefault();
    });
}