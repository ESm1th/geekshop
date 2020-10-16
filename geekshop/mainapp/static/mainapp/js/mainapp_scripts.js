window.onload = function() {
    $('.categories').on('click', $(this).find('a'), function(event) {
        
        var link = event.target.href;

        $.ajax({
            url: link,
            success: function(data) {
                $('.category_list').html(data.result);
            },
        });

        $(this).find('a').each(function() {
            $(this).removeClass();
        });

        $(event.target).addClass('checkmark');

        event.preventDefault();
    });
};