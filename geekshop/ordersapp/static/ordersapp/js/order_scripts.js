window.onload = function() {

    // updating total price and total items quantity on order header
    $('.order_item').on('focusin', 'input[type="number"]', function(event) {

        $(this).data('old_value', event.target.value);

    }).on('change', 'input[type="number"]', function(event) {


        var old_value = $(this).data('old_value');
        var new_value = $(this).val();
        var closest_div = $(this).closest('div');
        var total = parseInt($('.total_price').text());
        var quantity = parseInt($('.total_quantity').text());
        var price_exists = $(closest_div).children('p').text()

        if (old_value > new_value) {
            var differance = old_value - new_value;
            quantity -= differance;

            if (price_exists) {
                total = total - differance *
                    parseInt($(closest_div).children('p').text());
            };

        } else {
            var differance = new_value - old_value;
            quantity += differance;

            if (price_exists) {
                total = total + differance *
                    parseInt($(closest_div).children('p').text());
            };
        };

        $('.total_price').html(total);
        $('.total_quantity').html(quantity);
        $(this).blur();
    });

    // updating total items quantity on order header
    $('.order_item').on('change', 'select', function(event) {

        var num = 0

        $('.order_items').children('div').each(function() {
            title = $('option:selected', $(this).children('select')).text();
            if (title != '---------') {
                num += 1;
                $(this).children('input').attr('disabled', false);
            } else {
                $(this).children('input').val(0);
                $(this).children('input').attr('disabled', true);
            };
        });

        $('.total_items_quantity').html(num);
    });


    // $(document).on('change', $('.price'), function() {

    //     var sum = 0
    //     var items = $('.price');

    //     // for (i = 1; i < items.length; i++) {
    //     //     sum += parseInt(items[i].innerText);
    //     // };

    //     // console.log(sum);


    //     document.querySelectorAll('.order_item p').forEach(function(p) {
    //         sum += parseInt(p.innerText);
    //     });

    //     console.log(sum);
    // });


    $('.order_item').formset({
        addText: 'add item',
        deleteText: 'remove item',
        prefix: 'order_items',
    });


    $(document).on('change', 'select', function(event) {

        var init_object = event.target;
        var closest_div = init_object.closest('div');
        var sum = 0;

        if (event.target.value) {
            $.ajax({
                url: '/orders/item/get/price/' + event.target.value,
                success: function(data) {

                    if ($(closest_div).children('p').text() != Math.floor(data.price)) {
                        $(closest_div).children('p').text(Math.floor(data.price));
                    };
                },
            });

    
            // } else {
            //     $(closest_div).children('p').text(0);
        };
        document.querySelectorAll('.order_item p').forEach(function(p) {
                sum += parseInt(p.innerText);
            });

        

        console.log(sum);
        event.preventDefault();

    });
};