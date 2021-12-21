var priceFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'VND',
});

// expand product
$('.expand').click(function() {
    if ($(this).children('i').hasClass('fa-minus')) {
        $(this).children('i').removeClass('fa-minus');
        $(this).children('i').addClass('fa-plus');
    }
    else {
        $(this).children('i').removeClass('fa-plus');
        $(this).children('i').addClass('fa-minus');
    }
})
$('.seemore').click(function() {
    if ($(this).text() == 'See more') {
        $(this).text('See less');
    }
    else {
        $(this).text('See more');
    }
})


