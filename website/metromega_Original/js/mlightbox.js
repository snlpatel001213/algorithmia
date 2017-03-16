/* 
 Plugin     : Tileshow
 Version    : 1.1
 Created on : Aug 13, 2013
 Author     : Grozav http://grozav.com
 */

(function($) {
    $.fn.mlightbox = function(option) {

        var a = $(this);
        var $preloader = $('.mlightbox#loader');
        var $this = $($(this).attr('href'));
        function fbShare(url, title, descr, image, winWidth, winHeight) {
            var winTop = (screen.height / 2) - (winHeight / 2);
            var winLeft = (screen.width / 2) - (winWidth / 2);
            window.open('http://www.facebook.com/sharer.php?s=100&p[title]=' + title + '&p[summary]=' + descr + '&p[url]=' + url + '&p[images][0]=' + image, 'sharer', 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
        }
        function twitterShare(url, title, descr) {
            window.open('https://twitter.com/intent/tweet?url="' + url + '"&text=' + url + ' ' + title + ' ' + descr);
        }


        if (option == 'image') {

            function lightboxshow() {
                $this.fadeIn(1000);
                $details.css({
                    'right': -$details.width() + 'px'
                });
                $details.delay(500).animate({
                    'right': '0px'
                }, 500);
                $content.fadeIn(0);
            }

            var $content = $('.mlightbox-content', $this);
            var $details = $('.mlightbox-details', $this);
            var $image = $('img', $content);
            var href = a.attr('data-src');
            function updateImg() {
                var contentwidth = $content.width();
                var contentheight = $content.height();
                var imagewidth = $image.width();
                var imageheight = $image.height();
                var ratio = imageheight / imagewidth;
                if ((imagewidth / imageheight) > (contentwidth / contentheight)) {
                    $image.css("width", contentwidth);
                    $image.css("height", contentwidth * ratio);
                    var margintop = (contentheight - imageheight) / 2;
                    $image.css({
                        'margin-top': margintop,
                        'margin-left': 0
                    });
                } else {

                    $image.css("height", contentheight);
                    $image.css("width", contentheight * 1 / ratio);
                    var marginleft = (contentwidth - imagewidth) / 2;
                    $image.css({
                        'margin-top': 0,
                        'margin-left': marginleft
                    });
                }

            }

            $(window).resize(function() {
                updateImg();
            }).trigger('reisize');
            a.click(function() {

                if ($image.attr('src') != href) {
                    $image.attr('src', href);
                    $image.css({
                        'height': 'auto',
                        'width': 'auto'
                    });
                    $preloader.fadeIn();
                    var cancel = 0;
                    $preloader.click(function() {
                        $preloader.fadeOut();
                        cancel = 1;
                    });

                    var title = a.attr('data-title');
                    var description = a.attr('data-description');
                    $('.mlightbox-title').html(title);
                    $('.mlightbox-subtitle').html(description);
                    $image.load(function() {
                        if (cancel)
                            return false;
                        $preloader.fadeOut();
                        lightboxshow();
                        $(window).trigger('resize');
                    });
                } else {
                    lightboxshow();
                    $(window).trigger('resize');
                }
            });

            $content.click(function() {
                $this.fadeOut();
            });
        }
        else if (option == 'blog') {
            var $content = $('.blogpost-content', $this);
            var $details = $('.blogpost-details', $this);
            function lightboxshow2() {
                $this.fadeIn(1000);
                $details.css({
                    'right': -$details.width() + 'px'
                });
                $details.delay(500).animate({
                    'right': '0px'
                }, 500);
                $content.fadeIn(0);
            }

            var $load = a.attr('data-href') + ' .blogpost';
            a.click(function(e) {

                $this.empty();
                $preloader.fadeIn();
                var cancel = 0;
                $preloader.click(function() {
                    $preloader.fadeOut();
                    cancel = 1;
                });

                $($this).load($load, function() {
                    if (cancel)
                        return false;
                    $preloader.fadeOut();
                    lightboxshow2();
                    $('.blogpost-content', $this).mCustomScrollbar({
                        mouseWheelPixels: 300,
                        theme: 'dark',
                        scrollButtons: {
                            enable: true
                        },
                        advanced: {
                            autoExpandHorizontalScroll: true
                        }
                    });
                    $('.close-mlightbox', $this).on('click', function(e) {
                        $this.fadeOut();
                        $preloader.fadeOut();
                        e.preventDefault();
                        return false;
                    });


                });

                e.preventDefault();
            });

        }

        else if (option == 'video') {

            var $content = $('.mlightbox-content', $this);
            var $details = $('.mlightbox-details', $this);
            var $video = $('.fitvideo', $this);

            function lightboxshow3() {
                $this.fadeIn(1000);
                $details.css({
                    'right': -$details.width() + 'px'
                });
                $details.delay(500).animate({
                    'right': '0px'
                }, 500);
                $content.fadeIn(0);
            }

            a.click(function(e) {

                var title = a.attr('data-title');
                var description = a.attr('data-description');
                var src = a.attr('data-src');
                $('.mlightbox-title').html(title);
                $('.mlightbox-subtitle').html(description);
                $('iframe', $video).attr('src', src);

                $preloader.fadeIn();

                setTimeout(function(){
                    lightboxshow3();
                    $(window).trigger('resize');
                }, 500);

                $preloader.delay(500).fadeOut(500);

                
            });

            $video.fitVids();

            $(window).resize(function() {
                var contentheight = $content.height();
                var videoheight = $video.height();
                var margintop = (contentheight - videoheight) / 2;
                $video.css({
                    'margin-top': margintop,
                    'margin-left': 0
                });
            });

        }

        $('.close-mlightbox', $this).click(function(e) {
            $this.fadeOut();
            $preloader.fadeOut();
            e.preventDefault();
        });


    };
}(jQuery));