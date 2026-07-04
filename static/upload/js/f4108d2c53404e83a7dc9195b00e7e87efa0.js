    //top fixed
    $(window).scroll(function () {
        if ($(window).scrollTop() > 0) {
            $('#c_navigation_006_P_929-1718162480250').addClass('active')
        } else {
            $('#c_navigation_006_P_929-1718162480250').removeClass('active')
        }
    })

    $('#c_navigation_006_P_929-1718162480250').mouseenter(function () {
        $('#c_navigation_006_P_929-1718162480250').addClass('actives')
    }).mouseleave(function () {
        if ($(window).scrollTop() == 0) {
            $('#c_navigation_006_P_929-1718162480250').removeClass('actives')
        }
    });
    $('#c_navigation_006_P_929-1718162480250').mouseenter(function () {
      
       if ($(window).scrollTop() > 0) {
            $('#c_navigation_006_P_929-1718162480250').addClass('activess')
        } else if ($(window).scrollTop() == 0)  {
            $('#c_navigation_006_P_929-1718162480250').removeClass('activess')
        }
    });
  
  //language
$("#c_navigation_006_P_929-1718162480250").find("img").eq(1).addClass("logocai");
$(".head_lan .lan_con").hover(function () {
    $(this).find(".lan_list").addClass("cur");
  }, function () {
    $(this).find(".lan_list").removeClass("cur");
  })