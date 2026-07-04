//home banner
var swiperFlag = false;
var wyzVido = new Swiper('.homeLb .swiper-container', {
    autoplay: {
        delay: 5000,
        stopOnLastSlide: false,
        disableOnInteraction: true,
    },
    speed: 1200,
    loop: true,
    parallax: true,
    navigation: {
        nextEl: '.homeLb .p_btn_next ',
        prevEl: '.homeLb .p_btn_prev ',
    },
    pagination: {
        el: '.homeLb .p_pagenation',
        clickable: true,
    },
    // 切换完毕事件
    on: {
        init: function () {
        },
        slideChangeTransitionEnd: function () {

            var _this = $('.homeLb .swiper-container .swiper-slide').eq(this.activeIndex);
            // 执行一下
            if (!swiperFlag) {
                swiperFlag = true;
            } else {
                videoSelect(_this);
            }
        }
    }
});
videoSelect($('.homeLb .swiper-container .swiper-slide.swiper-slide-active'));

function videoSelect(_this) {
    var cc = _this.find('.videoContent .video').length;
    console.log(cc);
    if (cc) {
        wyzVido.autoplay.stop();
        _this.find('.videoContent .video').trigger('play');

        _this.find('video').bind('ended', function () {
            wyzVido.slideNext();
            wyzVido.autoplay.start();
        });
    }
}