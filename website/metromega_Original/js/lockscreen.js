$(function() {

    $(document).ready(function() {
        $('#locklogo').fadeIn(1000);
    });


    $('#lockscreen').click(function() {
        if ($(this).hasClass('lockslide')) {
            var winheight = $(window).height();
            $(this).animate({'top': -winheight + 'px'}, 1000, function() {
                $(this).hide(0);
            });
        }
        else
            $(this).fadeOut(1000);
    });

    $(window).load(function() {
        $('#lockloader').fadeOut(500);
        $('#lockscreen').delay(1000).trigger('click');
    });

});