$( window ).on( "load", function () {
    $('#alert-show').hide();
    $('#alert-show').fadeTo(2000, 500).slideUp(500, function () {
        $('#alert-show').slideUp(500);
    });
});

$( document ).ready(function() {
    console.log( "document loaded" );
});

$( window ).on( "load", function() {
    console.log( "window loaded" );
});