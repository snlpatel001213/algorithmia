/* 
 Plugin     : Tileshow
 Version    : 1.1
 Created on : Aug 13, 2013
 Author     : Grozav http://grozav.com
 */

(function($) {

    $.fn.tileshow = function(options) {

        var settings = $.extend({
            speed: 1000,
            timeout: 3000,
            autoplay: true,
            mousewheel: true
        }, options);

        var $this = $(this);

        var $current;

        var tiles = $('.slide', $this);

        var tileCount = tiles.length - 1;

        (function($) {
            $.timer = function(func, time, autostart) {
                this.set = function(func, time, autostart) {
                    this.init = true;
                    if (typeof func == 'object') {
                        var paramList = ['autostart', 'time'];
                        for (var arg in paramList) {
                            if (func[paramList[arg]] != undefined) {
                                eval(paramList[arg] + " = func[paramList[arg]]");
                            }
                        }
                        ;
                        func = func.action;
                    }
                    if (typeof func == 'function') {
                        this.action = func;
                    }
                    if (!isNaN(time)) {
                        this.intervalTime = time;
                    }
                    if (autostart && !this.isActive) {
                        this.isActive = true;
                        this.setTimer();
                    }
                    return this;
                };
                this.play = function(reset) {
                    if (!this.isActive) {
                        if (reset) {
                            this.setTimer();
                        } else {
                            this.setTimer(this.remaining);
                        }
                        this.isActive = true;
                    }
                    return this;
                };
                this.pause = function() {
                    if (this.isActive) {
                        this.isActive = false;
                        this.remaining -= new Date() - this.last;
                        this.clearTimer();
                    }
                    return this;
                };
                this.stop = function() {
                    this.isActive = false;
                    this.remaining = this.intervalTime;
                    this.clearTimer();
                    return this;
                };
                this.toggle = function(reset) {
                    if (this.isActive) {
                        this.pause();
                    } else if (reset) {
                        this.play(true);
                    } else {
                        this.play();
                    }
                    return this;
                };
                this.reset = function() {
                    this.isActive = false;
                    this.play(true);
                    return this;
                };
                this.clearTimer = function() {
                    window.clearTimeout(this.timeoutObject);
                };
                this.setTimer = function(time) {
                    var timer = this;
                    if (typeof this.action != 'function') {
                        return;
                    }
                    if (isNaN(time)) {
                        time = this.intervalTime;
                    }
                    this.remaining = time;
                    this.last = new Date();
                    this.clearTimer();
                    this.timeoutObject = window.setTimeout(function() {
                        timer.go();
                    }, time);
                };
                this.go = function() {
                    if (this.isActive) {
                        this.action();
                        this.setTimer();
                    }
                };

                if (this.init) {
                    return new $.timer(func, time, autostart);
                } else {
                    this.set(func, time, autostart);
                    return this;
                }
            };
        })(jQuery);

        function tile(index) {
            var current = $current;

            tiles.eq(index).fadeIn(settings.speed);
            tiles.eq(current).fadeOut(settings.speed);

            $current = index;

            count = 0;
        }


        tiles.fadeOut(0);

        var first = $('.active', $this).index();

        if (first != undefined)
            tile(first);
        else
            tile(0);


        if (settings.autoplay == true) {
            var count = 0;
            var timer = $.timer(function() {
                count++;
                if (count >= settings.timeout / 100) {
                    if ($current < tileCount) {
                        tile($current + 1);
                    } else
                        tile(0);
                }
            }, 100, true);

            if (settings.pauseOnHover == true) {
                $this.hover(function() {
                    timer.pause();
                }, function() {
                    timer.play();
                });
            }

        }



        $this.bind('mousewheel', function(event, delta) {
            if (delta < 0) {
                if ($current < tileCount) {
                    tile($current + 1);
                } else
                    tile(0);
            }
            if (delta > 0){
                if($current > 0){
                    tile($current - 1);
                }else
                    tile(tileCount);
            }
            
            return false;
        });





    };
}(jQuery));