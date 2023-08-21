function scrollToTop() {
    const scrollToTopName = 'scroll-to-top'
    const scrollToTopId = '#'+scrollToTopName
    const pxFromTop = 500

    $('#footer').append('<div id="'+scrollToTopName+'">Наверх страницы</div>')

    if ( $(window).scrollTop() > pxFromTop ) {
        $(scrollToTopId).fadeIn()
    } else {
        $(scrollToTopId).hide()
    }

    $(scrollToTopId).click((e) => {
        e.preventDefault()
        $('html, body').animate({scrollTop: 0}, 500)
    })

    $(window).scroll(function() {
        if ( $(this).scrollTop() > pxFromTop ) {
            $(scrollToTopId).fadeIn()
        } else {
            $(scrollToTopId).fadeOut()
        }
    })

}


export {scrollToTop}
