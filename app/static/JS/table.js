
$(window).on("load resize", function() {
    var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
        $('.tbl-header').css({'padding-right':scrollWidth});
}).resize();


let head = document.getElementsByTagName('thead')[0];

let body = document.getElementById('table_body');

function select_scroll_head(e){
    body.scrollLeft = head.scrollLeft;
}

function select_scroll_body(e){
    head.scrollLeft = body.scrollLeft;
}

head.addEventListener('scroll', select_scroll_head, false);
body.addEventListener('scroll', select_scroll_body, false);